from config import utils

db_handle = utils.db_handle
get_collection = utils.get_collection_handle

class SubwayInfo():

    def __init__(self):
        self.db_name = 'subway_elevator'
    
    def get_subway_elvtr(self, target):
        collection_elvtr = get_collection(db_handle, self.db_name)
        result = collection_elvtr.find({'sw_nm': target})
        result = list(result)

        ret = []
        for temp in result:
            data = {
                'sw_nm': temp['sw_nm'],
                'x': temp['x'],
                'y': temp['y']
            }
            ret.append(data)
        if not result:
            return {'message': 'No results'}
        return {'elvtr': ret}