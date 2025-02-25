from fastapi import APIRouter, WebSocket
import psutil
import asyncio
import time
# Store previous values for calculating speed
prev_net_io = psutil.net_io_counters()
prev_time = time.time()


router = APIRouter()




@router.get("/network-usage")
def get_network_usage():
    global prev_net_io, prev_time
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    elapsed_time = current_time - prev_time

    upload_speed = (current_net_io.bytes_sent - prev_net_io.bytes_sent) / elapsed_time
    download_speed = (current_net_io.bytes_recv - prev_net_io.bytes_recv) / elapsed_time

    # Update previous values
    prev_net_io = current_net_io
    prev_time = current_time

    return {
        "upload_speed": round(upload_speed, 2),       # Bytes sent per second
        "download_speed": round(download_speed, 2)    # Bytes received per second
    }



# CPU Usage Endpoint
@router.get("/cpu-usage")
async def get_cpu_usage():
    return {"cpu_usage": psutil.cpu_percent(interval=1)}

# Memory Usage Endpoint
@router.get("/memory-usage")
async def get_memory_usage():
    memory = psutil.virtual_memory()
    return {"memory_usage": memory.percent}

# Disk Usage Endpoint
@router.get("/disk-usage")
async def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {"disk_usage": disk.percent}

# WebSocket Endpoint for Real-time Updates
@router.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Gather all metrics
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            # Send metrics as JSON object
            await websocket.send_json({
                "cpu_usage": cpu,
                "memory_usage": memory,
                "disk_usage": disk
            })
            
            await asyncio.sleep(2)  # Update every 2 seconds
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
