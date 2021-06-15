import speedtest

s = speedtest.Speedtest()
s.get_config()
s.get_best_server()
speed_bps = s.download()
speed_mbps = round(speed_bps / 1000 / 1000, 1)
print(speed_mbps)