import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

gestures_dict = {
    1: "Help",
    2: "Medicine",
    3: "Washroom",
    4: "Water",
    0: "Cancel"   # FIST = Cancel
}

def fingers_up(hand_landmarks):
    tips = [8, 12, 16, 20]
    fingers = []

    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

cap = cv2.VideoCapture(0)

finger_count = 0
last_finger_count = -1

# For emergency light blinking
blink_state = True
last_blink_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # Sidebar
    cv2.rectangle(frame, (0, 0), (400, h), (50, 50, 50), -1)
    cv2.putText(frame, "NURSE CALL SYSTEM",
                (50, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 255), 2)

    y = 80
    cv2.putText(frame, "Help: 1 Finger", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.putText(frame, "Medicine: 2 Fingers", (20, y+40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.putText(frame, "Washroom: 3 Fingers", (20, y+80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.putText(frame, "Water: 4 Fingers", (20, y+120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.putText(frame, "Cancel: Fist", (20, y+160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    if result.multi_hand_landmarks:
        for hand_lms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, hand_lms, mp_hands.HAND_CONNECTIONS
            )

            fingers = fingers_up(hand_lms)
            count = fingers.count(1)
            finger_count = count

            if finger_count != last_finger_count:
                action = gestures_dict.get(finger_count)
                print("Nurse Alert Triggered:", action)
                last_finger_count = finger_count

                if finger_count == 0:
                    print("Cancelled. Closing video...")
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

    # -------- EMERGENCY LIGHT (HELP = 1) ----------
    if finger_count == 1:
        if time.time() - last_blink_time > 0.5:
            blink_state = not blink_state
            last_blink_time = time.time()

        if blink_state:
            color = (0, 0, 255)   # RED
        else:
            color = (255, 0, 0)   # BLUE

        cv2.rectangle(frame, (420, 200), (620, 350), color, -1)
        cv2.putText(frame, "EMERGENCY!",
                    (430, 380),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0,0,255), 3)

    # ---------------------------------------------

    cv2.putText(frame, f"FINGERS: {finger_count}",
                (420, 120), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow("Gesture Nurse Calling System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()