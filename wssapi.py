import asyncio
import websockets
import json
import random
import string
# WSS URI
wss_uri = "wss://fs.firefly.matce.cn/queue/join"
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
async def send_wss_request(uri, data_value, content):
    r_hash=generate_random_string(11)
    try:
        async with websockets.connect(uri) as websocket:
            # 第一个请求
            first_data, first_data2 = await handle_first_request(websocket, data_value, r_hash)
            if first_data is None or first_data2 is None:
                return None
            async with websockets.connect(uri) as websocket:
                # 第二个请求
                second_data = await handle_second_request(websocket, first_data, r_hash)
                if second_data is None:
                    return None
            async with websockets.connect(uri) as websocket:
                # 第三个请求
                result = await handle_third_request(websocket, first_data2, second_data, content, data_value, r_hash)
                return result
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed with exception: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

async def handle_first_request(websocket, data_value, r_hash):
    try:
        # 等待并处理第一个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "send_hash":
            # 发送 session_hash
            print("state 1")
            message = json.dumps({"fn_index": 1, "session_hash": r_hash})
            await websocket.send(message)

        # 等待并处理第二个消息
        response = await websocket.recv()
        print("state 2")

        # 等待并处理第三个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "send_data":
            print("state 3")
            # 发送数据
            message = json.dumps({
                "data": [data_value],
                "event_data": None,
                "fn_index": 1,
                "session_hash": r_hash
            })
            await websocket.send(message)

        # 等待并处理第四个消息
        response = await websocket.recv()
        print("state 5")

        # 等待并处理第五个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "process_completed":
            print("state 6")
            if len(data['output']['data'][1]) < 15:
                return await send_wss_request(wss_uri, data_value)
            else:
                return data['output']['data'][0], data['output']['data'][1]
    except Exception as e:
        print(f"An error occurred in handle_first_request: {e}")
        return None, None

async def handle_second_request(websocket, first_data,r_hash):
    try:
        # 等待并处理第一个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "send_hash":
            print("state 7")
            # 发送 session_hash
            message = json.dumps({"fn_index": 2, "session_hash": r_hash})
            await websocket.send(message)

        # 等待并处理第二个消息
        response = await websocket.recv()
        print("state 8")

        # 等待并处理第三个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "send_data":
            print("state 9")
            message = json.dumps({
                "data": [first_data],
                "event_data": None,
                "fn_index": 2,
                "session_hash": r_hash
            })
            await websocket.send(message)

        # 等待并处理第四个消息
        response = await websocket.recv()
        print("state 10")

        # 等待并处理第五个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "process_completed":
            print("state 11")
            first_param = data['output']['data'][0]['name']
            return first_param
    except Exception as e:
        print(f"An error occurred in handle_second_request: {e}")
        return None

async def handle_third_request(websocket, first_data2, second_data, content, data_value, r_hash):
    try:
        # 等待并处理第一个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "send_hash":
            print("state 12")
            message = json.dumps({"fn_index": 4, "session_hash": r_hash})
            await websocket.send(message)

        # 等待并处理第二个消息
        response = await websocket.recv()
        print("state 13")

        # 等待并处理第三个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "send_data":
            print("state 14")
            message = json.dumps({ #构建提交的json
                "data": [
                    content,
                    True,
                    {
                        "name": second_data,
                        "data": "https://fs.firefly.matce.cn/file=" + second_data,
                        "is_file": True,
                        "orig_name": "audio.wav"
                    },
                    first_data2,
                    0,
                    48,
                    0.6,
                    1.6,
                    0.7,
                    data_value
                ],
                "event_data": None,
                "fn_index": 4,
                "session_hash": r_hash
            })
            await websocket.send(message)

        # 等待并处理第四个消息
        response = await websocket.recv()
        print("state 15")
        
        # 等待并处理第五个消息
        response = await websocket.recv()
        print("state 16")
        
        # 等待并处理第六个消息
        response = await websocket.recv()
        data = json.loads(response)
        if data.get('msg') == "process_completed":
            print("state 17")
            return "https://fs.firefly.matce.cn/file=" + data['output']['data'][0]['name']
    except Exception as e:
        print(f"An error occurred in handle_third_request: {e}")
        return None

async def run_predict(speaker, text):
    result = await send_wss_request(wss_uri, speaker, text)
    return result