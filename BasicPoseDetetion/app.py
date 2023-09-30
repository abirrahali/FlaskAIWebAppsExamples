from cv2 import VideoCapture
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import atexit

app = Flask(__name__)

# Create separate video capture objects for face and hand detection
cap_hands = VideoCapture(0)
cap_face = VideoCapture(0)
# cap_pose = VideoCapture(0)

def release_video_capture_objects():
    """Release video capture objects."""
    cap_hands.release()
    cap_face.release()
    # cap_pose.release()

def gen_frames_hands():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    while True:
        cap_hands.open(0)  # Open the camera capture
        while cap_hands.isOpened():
            success, image = cap_hands.read()
            if not success:
                print("Ignoring empty camera frame.")
                cap_hands.release()  # Release the camera capture
                break

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
                results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing_styles.get_default_hand_landmarks_style(),
                                              mp_drawing_styles.get_default_hand_connections_style())

            ret, jpeg = cv2.imencode('.jpg', cv2.flip(image, 1))
            if ret:
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap_hands.release()

# def gen_frames_pose():
#     ## initialize pose estimator
#     mp_drawing = mp.solutions.drawing_utils
#     mp_drawing_styles = mp.solutions.drawing_styles
#     mp_pose = mp.solutions.pose
#     pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    # while True:
    #     cap_pose.open(0)  # Open the camera capture
    #     while cap_pose.isOpened():
    #         success, image = cap_pose.read()
    #         if not success:
    #             print("Ignoring empty camera frame. @@@@@@@@@@@@@@")
    #             cap_pose.release()  # Release the camera capture
    #             break

    #         image.flags.writeable = False
    #         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #         with mp_pose.pose(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    #             results = pose.process(image)

    #         image.flags.writeable = True
    #         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #         print(results)

    #         if results.multi_pose_landmarks:
    #             for pose_landmarks in results.multi_pose_landmarks:
    #                 mp_drawing.draw_landmarks(image, pose_landmarks, mp_pose.POSE_CONNECTIONS,
    #                                           mp_drawing_styles.get_default_pose_landmarks_style(),
    #                                           mp_drawing_styles.get_default_pose_connections_style())

    #         ret, jpeg = cv2.imencode('.jpg', cv2.flip(image, 1))
    #         if ret:
    #             frame = jpeg.tobytes()
    #             yield (b'--frame\r\n'
    #                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    #     cap_pose.release()

def gen_frames_face():
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    while True:
        cap_face.open(0)  # Open the camera capture
        while cap_face.isOpened():
            success, image = cap_face.read()
            if not success:
                print("Ignoring empty camera frame.")
                cap_face.release()  # Release the camera capture
                break

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            with mp_face_mesh.FaceMesh(
                    static_image_mode=True,
                    refine_landmarks=True,
                    max_num_faces=2,
                    min_detection_confidence=0.5) as face_mesh:
                results = face_mesh.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())

            ret, jpeg = cv2.imencode('.jpg', cv2.flip(image, 1))
            if ret:
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap_face.release()

@app.route('/video_feed/<detection_type>')
def video_feed(detection_type):
    if detection_type == 'hands':
        return Response(gen_frames_hands(), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif detection_type == 'face':
        return Response(gen_frames_face(), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif detection_type == 'pose':
        return Response(gen_frames_pose(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Invalid detection type"

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

if __name__ == '__main__':
    atexit.register(release_video_capture_objects)
    app.run(debug=True)
