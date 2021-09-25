from bot.device import Device
from bot.hub import JobHub, ServiceHub
from service.screen_capture import SCREEN_SHOW

if __name__ == '__main__':
    new_device = Device()
    service_hub = ServiceHub(new_device)
    job_hub = JobHub(new_device, service_hub)

    job_hub.change_map_view.execute()
    job_hub.sleep(1)
    job_hub.click_storage.execute()
    job_hub.click_center.execute()

    service_hub.screen_capture.execute(SCREEN_SHOW, resize=True)
