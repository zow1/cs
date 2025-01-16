import subprocess  
  
# 定义FFmpeg命令  
ffmpeg_command = [  
    'ffmpeg',  
    '-re',  
    '-stream_loop', '-1',  
    '-i', 'https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1737053867/ei/SwKJZ_6ACIz1s8IPuqTXkQo/ip/13.213.152.249/id/V1p33hqPrUk.58/source/yt_live_broadcast/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/hfr/1/playlist_duration/30/manifest_duration/30/maxh/4320/maudio/1/siu/1/bui/AY2Et-P-p5OypuI2fhfW5Q0QVp1-YfNQ7SAeTEX7-6veveU5UvukxPaQBx99AjWZD3OgHgbI9w/spc/9kzgDSvCUC8Jp4YRb5cm9Mwp4j1f9Ea0dcBpkR3MBGIII1vx-JHRTenH0yRm0P181Zi5zDQDUXCg/vprv/1/go/1/rqh/5/pacing/0/nvgoi/1/keepalive/yes/fexp/51326932%2C51335594%2C51353498%2C51355912%2C51384461/dover/11/itag/0/playlist_type/DVR/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Chfr%2Cplaylist_duration%2Cmanifest_duration%2Cmaxh%2Cmaudio%2Csiu%2Cbui%2Cspc%2Cvprv%2Cgo%2Crqh%2Citag%2Cplaylist_type/sig/AJfQdSswRQIgerOvgDQKBjQdS4AZH3KjTtDM8J6X2vmXmMgvxwBr_A4CIQC7thYvir2EaiFzOP9nAxlo4OVRrrBH7S4gdnOr78N1yg%3D%3D/file/index.m3u8',  # 替换为你的输入流URL  
    '-bsf:a', 'aac_adtstoasc',  
    '-vcodec', 'copy',  
    '-acodec', 'copy',  
    '-f', 'flv',  
    '-y',  
    '-reconnect', '1',  
    '-reconnect_at_eof', '1',  
    '-reconnect_streamed', '1',  
    'rtmp://ali.push.yximgs.com/live/feicui'  # 替换为你的推流服务器地址  
]   #播放地址http://ali.hlspull.yximgs.com/live/feicui.flv
  
# 使用subprocess启动FFmpeg进程  
try:  
    process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE)  
    # 你可以在这里添加代码来监控FFmpeg进程的输出或错误  
    # 例如，读取stderr来查看FFmpeg的日志输出  
    while True:  
        line = process.stderr.readline().decode('utf-8').strip()  
        if not line:  
            break  
        print(line)  
    process.wait()  # 等待FFmpeg进程结束  
except Exception as e:  
    print(f"An error occurred: {e}")
