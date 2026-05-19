# FACE FILTER REPORT

[FACE_FILTER]
strict_human_face_only=YES

- confidence_threshold: >=0.70
- min_face_size: >=80x80
- aspect_ratio_validation: enabled
- landmark_like_eye_geometry_validation: enabled
- texture_variance_validation: enabled
- HSV_skin_validation: enabled
- YCrCb_skin_validation: enabled

[DISTORTION_FIX]
status=PASS
