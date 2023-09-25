from .population_real_time import Population_real_time
from .population_ai_model import Population_AI_model

class Custom_info():
    
    def __init__(self):
        self.custom_list = ['custom-demo', 'custom-elevator', 'custom-population',
                            'custom-predict', 'custom-safety', 'custom-safey-loc',
                            'custom-low-bus', 'custom-festival']

    def get_custom_info(self, id, collection):
        ret = []
        custom = self.get_id_info_to_custom(id, collection)
        # print(custom)
        for target in self.custom_list:
            if custom[target]:
                ret.append({target: self.get_target_matching_info(target)})
        return ret

    def get_id_info_to_custom(self, id, collection):
        user_info = collection.find_one({'ID': id})
        if user_info == None:
            raise ValueError(f"Not exist user: {id}")
        return user_info['custom']

    def get_target_matching_info(self, target):

        from config import utils
        from pymongo.errors import PyMongoError

        db_handle = utils.db_handle
        get_collection = utils.get_collection_handle

        if target == self.custom_list[0]:
            collection = get_collection(db_handle, 'demo')
            data_demo = list(collection.find({}))
            ret = []
            for item in data_demo:
                item_data = {
                    "location": str(item["location"]),
                    "date": str(item["date"]),
                    "time": str(item["time"]),
                    "amount": str(item["amount"])
                }
                ret.append(item_data)
            return ret
        elif target == self.custom_list[1]:  # subway elevator
            return ret
        elif target == self.custom_list[2]:  # We have to select region
            prt = Population_real_time()
            collection = get_collection(db_handle, 'popul_real_time_reg')
            region_info = list(collection.find({}))
            ret = prt.get_real_time_popul(region_info)
            return ret
        elif target == self.custom_list[3]:
            popul_ai = Population_AI_model()
            ret = popul_ai.return_predict_value()
            return ret
        elif target == self.custom_list[4]:
            return ret
        elif target == self.custom_list[5]:
            collection = get_collection(db_handle, 'safety_guard_house')
            ret = collection.find()
            ret_list = [{'name': item['name'], 'x': item['y'], 'y': item['x']}
                        for item in ret]
            return ret_list
        elif target == self.custom_list[6]:  # What we have to show?

            return ret
        elif target == self.custom_list[7]:

            return ret
        else:
            raise ValueError(f"Invalid custom element : {target}")
