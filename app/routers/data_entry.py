from fastapi import APIRouter
from app.services.read_data_sensor import RequestSensor
from dotenv import load_dotenv
from app.services.sensor_service import calculate_average_metrics
from app.services.read_data_factory import nested_data_factory ,get_factory_infor
from typing import List, Dict, Any
from app.services.token_service import check_valid_token
from datetime import date
from token_store import get_token, set_token
import asyncio


# Create a global lock
processing_lock = asyncio.Lock()
processed_data = None  # store result after process finishes

router = APIRouter()


report_lock = asyncio.Lock()
cached_report = None

@router.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


@router.get("/token-request")
async def token_request(token: str):
    result = check_valid_token(token=token)
    
    if result["status"] == "success":
        old_token = get_token()
        if old_token:
            print("Old token removed from memory:", old_token)
        
        # Store new token (overwrites old one)
        set_token(token)
        print("New token stored in memory:", get_token())
    else:
        print("Invalid token attempt:", token)
    
    return result

@router.get("/report")
async def get_reports():
    global cached_report

    token = get_token()
    if not token:
        return {"status": "error", "message": "No token stored"}

    result = check_valid_token(token)
    if result["status"] != "success":
        return result

    # Use lock to prevent multiple requests from running the same process
    async with report_lock:
        if cached_report:
            # If report is already generated, return cached report
            return cached_report

        all_reports: List[Dict[str, Any]] = []
        station_data = nested_data_factory(result["data"])
        sensor_data = RequestSensor(token)
        today_str = date.today()
        num = 0

        for ind in station_data:
            for i in ind['factory']:
                num += 1

                fc_dt = sensor_data._read_and_process_data(i['deviceId'])
                if fc_dt.empty:
                    avg_param = {
                        "ph": None,
                        "cod": None,
                        "ss": None,
                        "waterFlow": None,
                        "temperature": None
                    }
                else:
                    avg_param = calculate_average_metrics(fc_dt)

                station_ = get_factory_infor(i['deviceId'], station_data)

                single_factory_rp = {
                    "avg_parame": avg_param,
                    "date": today_str,
                    "device_ids": i['deviceId'],
                    "station_info": station_,
                }
                all_reports.append(single_factory_rp)
                print(num)

        cached_report = {"data": all_reports, "total_factories": len(all_reports)}
        return cached_report
