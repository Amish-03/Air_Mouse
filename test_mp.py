

try:
    import mediapipe as mp
    print("MediaPipe File:", mp.__file__)
    print("MediaPipe Path:", mp.__path__)

    try:
        from mediapipe import solutions
        print("Imported solutions via from mediapipe")
    except ImportError:
        print("Failed to import solutions via from mediapipe")

    try:
        import mediapipe.python.solutions as solutions
        print("Imported mediapipe.python.solutions")
        print(dir(solutions))
    except ImportError as e:
        print(f"Failed to import mediapipe.python.solutions: {e}")

    print("Solutions attribute on mp:", getattr(mp, 'solutions', 'NOT FOUND'))
except Exception as e:
    print(e)
