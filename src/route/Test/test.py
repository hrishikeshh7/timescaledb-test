from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from loguru import logger
import psycopg2.extras
from .. import get_raw_db
from datetime import datetime, timedelta

router = APIRouter()
import random


class Add(BaseModel):
    site: int
    panel: int
    device: int
    zone: int


"""
        new_update = table(
            site=info.site,
            panel=info.panel,
            device_code=info.device_code,
            zone=info.zone,
            value=info.value

        )
        db.add(new_update)
        db.commit()
"""


def generate_data_for_zone(site, panel, device, zone, rdb):
    try:
        value = 0
        time_limit_min = 525600  # 1 Year
        curr_time = datetime.now().replace(hour=0, minute=0, second=0)

        while time_limit_min > 0:
            entry_time = curr_time - timedelta(minutes=time_limit_min)
            entry_time = entry_time.replace(microsecond=0).isoformat()
            value = value + random.randint(0, 25)
            logger.info(
                f"Time:{entry_time} || Site:{site},Panel:{panel},Device:{device},Zone:{zone}--->Value:{value}")
            time_limit_min = time_limit_min - 30

            cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = f""" 
            insert into testdata (site,panel,device_code,zone_,time_,value_) 
            values 
            ({site}, '{panel}', '{device}', '{zone}', '{entry_time}', {value})"""

            cursor.execute(query)
            rdb.commit()
        proc_time = datetime.now() - curr_time
        logger.debug(f"Process Time for 1 Zone: {proc_time}")




    except Exception as e:
        logger.error(f"{e}")
        raise e


@router.post('/create/test', tags=["timescale"])
def add(
        info: Add,
        rdb: Session = Depends(get_raw_db)
):
    """
    site: int = 2
    panel: int = 2
    device_code: int = 20
    zone: int = 10

    :param info:
    :param db:
    :return:
    """
    try:
        for site in range(1, info.site + 1):
            # For one site

            for panel in range(1, info.panel + 1):
                # For one panel
                panel_name = "pan_" + str(panel)

                for device in range(1, info.device + 1):
                    # for one device
                    dev_name = "dev_" + str(device)

                    for zone in range(1, info.zone + 1):
                        # For one Zone
                        zone_name = "zone_" + str(zone)

                        generate_data_for_zone(site, panel_name, dev_name, zone_name, rdb)

                        pass

        pass
    except HTTPException as e:
        logger.error(f'{e}')
        raise e
    except Exception as e:
        logger.error(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')
