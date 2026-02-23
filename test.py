import sys

if sys.version_info.major==3 and sys.version_info.minor!=14:
    # Code that requires Python 3.9+
    print("Running new functionality")
else:
    # Fallback or skip
    print("Feature disabled on Python < 3.9")
