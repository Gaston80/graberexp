import redis
Nodes = [
        ["ExposureTime", 200],
        ["DeviceScanType", "Linescan3D"],
        #["Width", 5120],
        #["ReverseX", False],
        #["ReverseY", False],
        #["DecimationHorizontal", "DecimationHorizontal2"],
        #["AcquisitionFrameRateEnable", True],
        #["AcquisitionFrameRate", 1300],
        ["TriggerMode", "On"],
        #["TriggerSource", "Line0"]
    ]


blackLevel = 30
Redis = redis.StrictRedis(host='192.168.113.1', port=6379, db=0)

camSettings = {}
image_path = '/mnt/data/images'
Cams = []
