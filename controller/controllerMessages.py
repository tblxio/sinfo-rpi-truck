import time
# Drive left msg 100% power (angular motor clockwise)
drive_msgd = {
    "sbrick_id": "88:6B:0F:80:29:D1",  # "string. SBrick ID. <sbrick MAC>",
    "channel": "00",  # " string. hex string. the LEGO power function port you
                      # want to drive. <00|01|02|03>",
    "direction": "00",  # "string. clockwise or counterclockwise. <00|01>",
    "power": "f6",  # "string. hex string. FF means 100% speed. <00~FF>",
    "exec_time": 0.1,  # "number. seconds. 5566 means forever."
    "timestamp": time.time()  # "number. seconds. 5566 means forever."
}
# Drive right msg 100% power (angular motor anti-clockwise)
drive_msga = {
    "sbrick_id": "88:6B:0F:80:29:D1",  # "string. SBrick ID. <sbrick MAC>",
    "channel": "00",  # " string. hex string. the LEGO power function port you
                      # want to drive. <00|01|02|03>",
    "direction": "01",  # "string. clockwise or counterclockwise. <00|01>",
    "power": "f6",  # "string. hex string. FF means 100% speed. <00~FF>",
    "exec_time": 0.1,  # "number. seconds. 5566 means forever."
    "timestamp": time.time()
}
# Drive forward msg 100% power (linear motor clockwise)
drive_msgw = {
    "sbrick_id": "88:6B:0F:80:29:D1",  # "string. SBrick ID. <sbrick MAC>",
    "channel": "02",  # " string. hex string. the LEGO power function port you
                      # want to drive. <00|01|02|03>",
    "direction": "00",  # "string. clockwise or counterclockwise. <00|01>",
    "power": "f6",  # "string. hex string. FF means 100% speed. <00~FF>",
    "exec_time": 15,  # "number. seconds. 5566 means forever."
    "timestamp": time.time()
}
# Drive back msg 100% power (linear motor anti-clockwise)
drive_msgs = {
    "sbrick_id": "88:6B:0F:80:29:D1",  # "string. SBrick ID. <sbrick MAC>",
    "channel": "02",  # " string. hex string. the LEGO power function port you
                      # want to drive. <00|01|02|03>",
    "direction": "01",  # "string. clockwise or counterclockwise. <00|01>",
    "power": "f6",  # "string. hex string. FF means 100% speed. <00~FF>",
    "exec_time": 15,  # "number. seconds. 5566 means forever."
    "timestamp": time.time()
}
# Stop linear motor
stop_msg_l = {
    "sbrick_id": "88:6B:0F:80:29:D1",  # "string. SBrick ID. <sbrick MAC>",
    "channel": "02",  # " string. hex string. the LEGO power function port you
                      # want to drive. <00|01|02|03>",
    "direction": "00",  # "string. clockwise or counterclockwise. <00|01>",
    "power": "00",  # "string. hex string. FF means 100% speed. <00~FF>",
    "exec_time": 15  # "number. seconds. 5566 means forever."
}
# Stop angular motor
stop_msg_a = {
    "sbrick_id": "88:6B:0F:80:29:D1",  # "string. SBrick ID. <sbrick MAC>",
    "channel": "00",  # " string. hex string. the LEGO power function port you
                      # want to drive. <00|01|02|03>",
    "direction": "00",  # "string. clockwise or counterclockwise. <00|01>",
    "power": "00",  # "string. hex string. FF means 100% speed. <00~FF>",
    "exec_time": 15  # "number. seconds. 5566 means forever."
}


# Stop motors msg
stop_msg = {
    "sbrick_id": "88:6B:0F:80:29:D1",  # "string. SBrick ID. <sbrick MAC>",
    # " string. hex string. the LEGO power function port you
    #                    # want to drive. <00|01|02|03>",
    "channels": ['00']
}
# Get adc info(must be subscribed to the resp_topic elsewhere)
get_adc = {'status': 0, 'req_msg': '{"sbrick_id": "88:6B:0F:80:29:D1"}',
           'resp_topic': 'truck1/motor'}
