import RPi.GPIO as GPIO
import time
import threading
from mpu6050 import mpu6050
import csv
from TCP_sender import TCP_sender

class MotorController:
    def __init__(self):
        # === Tanımlar ===
        self.IN1, self.IN2, self.ENA = 17, 18, 12  # Sol motor
        self.IN3, self.IN4, self.ENB = 22, 23, 13  # Sağ motor
        self.BACKWARD_TRIG, self.BACKWARD_ECHO = 27, 25
        self.FORWARD_TRIG, self.FORWARD_ECHO = 26, 24
        self.ENC_A = 16
        self.servo_pin = 1

        self.PWM_FREQ = 1000  # Hz
        self.ENCODER_TICKS_PER_CM = 0.942
        self.DISTANCE_THRESHOLD = 10  # cm

        self.encoder_count = 0
        self.running = True
        self.integral = 0
        self.last_error = 0

        self.mpu = mpu6050(0x68)

        # GPIO ayarları
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm_servo = GPIO.PWM(self.servo_pin, 50)
        self.pwm_servo.start(0)

        for pin in [self.IN1, self.IN2, self.IN3, self.IN4, self.ENA, self.ENB, self.FORWARD_TRIG, self.BACKWARD_TRIG]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        GPIO.setup(self.FORWARD_ECHO, GPIO.IN)
        GPIO.setup(self.BACKWARD_ECHO, GPIO.IN)
        GPIO.setup(self.ENC_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.pwm_ENA = GPIO.PWM(self.ENA, self.PWM_FREQ)
        self.pwm_ENB = GPIO.PWM(self.ENB, self.PWM_FREQ)
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

        # Encoder thread
        self.encoder_thread = threading.Thread(target=self._encoder_thread)
        self.encoder_thread.start()

    # === Encoder thread ===
    def _encoder_thread(self):
        prev = GPIO.input(self.ENC_A)
        while self.running:
            curr = GPIO.input(self.ENC_A)
            if prev == GPIO.HIGH and curr == GPIO.LOW:
                self.encoder_count += 1
            prev = curr
            time.sleep(0.001)

    # === Fonksiyonlar ===
    def read_encoder_distance(self):
        return self.encoder_count / self.ENCODER_TICKS_PER_CM

    def read_encoder_speed(self, last_count, last_time):
        now = time.time()
        dc = self.encoder_count - last_count
        dt = now - last_time
        if dt < 0.01:
            return 0, self.encoder_count, now
        speed_cm_s = (dc / self.ENCODER_TICKS_PER_CM) / dt if dt != 0 else 0
        return speed_cm_s, self.encoder_count, now

    def measure_distance(self, TRIG, ECHO):
        GPIO.output(TRIG, 0)
        time.sleep(0.01)
        GPIO.output(TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG, 0)

        start = time.time()
        while GPIO.input(ECHO) == 0:
            if time.time() - start > 0.05:
                return 400
        pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            if time.time() - pulse_start > 0.05:
                return 400
        pulse_end = time.time()
        return (pulse_end - pulse_start) * 17150

    def stop(self, db, processor, duration=None):
        for pin in [self.IN1, self.IN2, self.IN3, self.IN4]:
            GPIO.output(pin, 0)
        self.pwm_ENA.ChangeDutyCycle(0)
        self.pwm_ENB.ChangeDutyCycle(0)

        if duration:
            message = f'{duration} saniye bekleniyor.'
            processor.speech(message)
            threading.Thread(target=TCP_sender, args=("bekle",), daemon=True).start()
            threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": message}}), daemon=True).start()
            threading.Thread(target=db.insert_document, args=("gorev_gecmisi", {"gecmis": message}), daemon=True).start()
            time.sleep(duration)

    def set_motor_direction(self, forward=True):
        GPIO.output(self.IN1, 1 if forward else 0)
        GPIO.output(self.IN2, 0 if forward else 1)
        GPIO.output(self.IN3, 1 if forward else 0)
        GPIO.output(self.IN4, 0 if forward else 1)

    def pid_control(self, target, actual, kp=12, ki=0.08, kd=1.2, dt=0.05):
        error = target - actual
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        self.last_error = error
        duty = kp * error + ki * self.integral + kd * derivative
        return max(min(duty, 50), 0)

    def calculate_max_speed(self, total_value, reference, max_speed, bool_flag):
        ramp_portion = 0.05
        ramp_length = ramp_portion * total_value
        if bool_flag == False:
            if reference < ramp_length:
                return max(20, max_speed * (reference / ramp_length))
            elif reference > total_value - ramp_length:
                return max(20, max_speed * ((total_value - reference) / ramp_length))
            else:
                return max_speed
        else:
            if reference < ramp_length:
                return max(20, max_speed * (reference / ramp_length))
            elif total_value < 70:
                return max(20, max_speed * ((total_value - reference) / ramp_length))
            else:
                return max_speed

    def speed_profile(self, distance_traveled, total_distance, elapsed_time, total_time, max_speed, TRIG, ECHO):
        if total_distance is not None:
            return self.calculate_max_speed(total_distance, distance_traveled, max_speed, False)
        elif total_time is not None:
            return self.calculate_max_speed(total_time, elapsed_time, max_speed, False)
        else:
            return self.calculate_max_speed(self.measure_distance(TRIG, ECHO), distance_traveled, max_speed, True)

    def saga_raw(self, hiz):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(hiz)
        self.pwm_ENB.ChangeDutyCycle(hiz)

    def sola_raw(self, hiz):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(hiz)
        self.pwm_ENB.ChangeDutyCycle(hiz)
    
    def go(self, db, processor, action: str, distance: float = None, duration: float = None, limit: float = None):
        self.encoder_count = 0
        self.integral = 0
        self.last_error = 0
        pid_log = []

        self.set_motor_direction(forward=(action == "forward"))
        start_time = time.time()
        last_count = 0
        last_time = time.time()
        max_speed = 87  # cm/s
        reaction_time = 0.5  # saniye
        buffer_distance = 10  # cm
        dt = 0.05

        if action == "forward":
            threading.Thread(target=TCP_sender, args=("ileri",), daemon=True).start()
            threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": "Araba ileri gidiyor."}}), daemon=True).start()
            isForward = True
        else:
            threading.Thread(target=TCP_sender, args=("geri",), daemon=True).start()
            threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": "Araba geri gidiyor."}}), daemon=True).start()
            isForward = False

        while True:
            now = time.time()
            elapsed = now - start_time
            current_distance = self.read_encoder_distance()
            actual_speed, last_count, last_time = self.read_encoder_speed(last_count, last_time)

            if isForward:
                obstacle_distance = self.measure_distance(self.FORWARD_TRIG, self.FORWARD_ECHO)
                target_speed = self.speed_profile(current_distance, distance, elapsed, duration, max_speed, self.FORWARD_TRIG, self.FORWARD_ECHO)
            else:
                obstacle_distance = self.measure_distance(self.BACKWARD_TRIG, self.BACKWARD_ECHO)
                target_speed = self.speed_profile(current_distance, distance, elapsed, duration, max_speed, self.BACKWARD_TRIG, self.BACKWARD_ECHO)

            braking_distance = actual_speed * reaction_time + buffer_distance

            if obstacle_distance <= braking_distance:
                print(f"Engel {obstacle_distance:.1f} cm mesafede, fren mesafesi {braking_distance:.1f} cm. Duruluyor.")
                self.stop(db, processor)
                processor.speech("Engel tespit edildi, motor durduruldu.")
                threading.Thread(target=TCP_sender, args=("engel",), daemon=True).start()
                threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": "Engel tespit edildi, motor durduruldu."}}), daemon=True).start()
                threading.Thread(target=db.insert_document, args=("gorev_gecmisi", {"gecmis": "Engel tespit edildi, motor durduruldu."}), daemon=True).start()
                break

            if distance and limit and elapsed >= limit:
                print("Zaman limiti aşıldı.")
                self.stop(db, processor)
                threading.Thread(target=TCP_sender, args=("dur",), daemon=True).start()
                threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": "Motor durduruldu."}}), daemon=True).start()
                threading.Thread(target=db.insert_document, args=("gorev_gecmisi", {"gecmis": "İstenilen mesafeye gidemeden zaman limiti aşıldı."}), daemon=True).start()
                processor.speech("İstenilen mesafeye gidemeden zaman limiti aşıldı.")
                break

            if duration and limit and current_distance >= limit:
                print("Mesafe limiti aşıldı.")
                self.stop(db, processor)
                threading.Thread(target=TCP_sender, args=("dur",), daemon=True).start()
                threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": "Motor durduruldu."}}), daemon=True).start()
                threading.Thread(target=db.insert_document, args=("gorev_gecmisi", {"gecmis": "İstenilen sürede gidemeden mesafe limiti aşıldı."}), daemon=True).start()
                processor.speech("İstenilen sürede gidemeden mesafe limiti aşıldı.")
                break

            if distance and current_distance >= distance:
                print("Hedef mesafe tamamlandı.")
                self.stop(db, processor)
                threading.Thread(target=TCP_sender, args=("dur",), daemon=True).start()
                threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": "Motor durduruldu."}}), daemon=True).start()
                threading.Thread(target=db.insert_document, args=("gorev_gecmisi", {"gecmis": f'{distance} cm mesafe başarıyla tamamlandı.'}), daemon=True).start()
                processor.speech("Hedef mesafe başarıyla tamamlandı.")
                break

            if duration and elapsed >= duration:
                print("Süre doldu.")
                self.stop(db, processor)
                threading.Thread(target=TCP_sender, args=("dur",), daemon=True).start()
                threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": "Motor durduruldu."}}), daemon=True).start()
                threading.Thread(target=db.insert_document, args=("gorev_gecmisi", {"gecmis": f'{duration} saniyelik mesafe başarıyla tamamlandı.'}), daemon=True).start()
                processor.speech("İstenilen süre başarıyla gidildi")
                break

            duty = self.pid_control(target_speed, actual_speed, kp=12, ki=0.01, kd=1.2, dt=dt)
            pid_log.append((time.time(), target_speed, actual_speed, duty))
            self.pwm_ENA.ChangeDutyCycle(duty)
            self.pwm_ENB.ChangeDutyCycle(duty)

        print("Araç durdu.")

        with open("pid_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "target_speed", "actual_speed", "duty"])
            writer.writerows(pid_log)

    def turn(self, db, target_angle, processor):
        angle_x = 0.0
        integral = 0.0
        last_error = 0.0
        Kp, Ki, Kd = 1.2, 0.05, 0.5

        if target_angle > 0:
            threading.Thread(target=TCP_sender, args=("sag",), daemon=True).start()
            message = f'{target_angle} derece sağa dönülüyor.'
        else:
            threading.Thread(target=TCP_sender, args=("sol",), daemon=True).start()
            message = f'{abs(target_angle)} derece sola dönülüyor.'

        processor.speech(message)
        threading.Thread(target=db.update_data, args=("arac_durumu", {"$set": {"durum": message}}), daemon=True).start()
        threading.Thread(target=db.insert_document, args=("gorev_gecmisi", {"gecmis": message}), daemon=True).start()

        previous_time = time.time()

        while True:
            current_time = time.time()
            dt = current_time - previous_time
            previous_time = current_time

            gyro_data = self.mpu.get_gyro_data()
            gyro_x = gyro_data['x'] + 5.2  # offset
            angle_x += gyro_x * dt

            error = abs(target_angle) - abs(angle_x)
            if error <= 0.5:
                break

            integral += error * dt
            derivative = (error - last_error) / dt if dt > 0 else 0
            output = Kp * error + Ki * integral + Kd * derivative
            last_error = error

            pwm_val = max(50, min(abs(output), 100))

            if target_angle > 0:
                self.saga_raw(pwm_val)
            else:
                self.sola_raw(pwm_val)

        self.stop(db, processor)
        print("Dönüş tamamlandı.")



    
