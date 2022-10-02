from datetime import datetime


def complete_data(request_data):
    req_time_updated = datetime.strptime(request_data.get('time_updated'),
                                         "%m/%d/%Y")
    req_time_created = datetime.strptime(request_data.get('time_created'),
                                         "%m/%d/%Y")
    request_data['time_updated'] = req_time_updated
    request_data['time_created'] = req_time_created
    return request_data
