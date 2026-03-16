import json
class Field:
    def __init__(self,field_type=str,required=True,default=None):
        self.type=field_type;self.required=required;self.default=default
class Serializer:
    def __init__(self): self._fields={}
    def field(self,name,**kwargs): self._fields[name]=Field(**kwargs)
    def serialize(self,obj):
        result={}
        for name,field in self._fields.items():
            val=obj.get(name,field.default) if isinstance(obj,dict) else getattr(obj,name,field.default)
            if val is not None: result[name]=field.type(val)
            elif field.required: raise ValueError(f"Missing required field: {name}")
        return result
    def deserialize(self,data):
        result={}
        for name,field in self._fields.items():
            if name in data:
                result[name]=field.type(data[name])
            elif field.required: raise ValueError(f"Missing: {name}")
            else: result[name]=field.default
        return result
    def many(self,items): return [self.serialize(i) for i in items]
if __name__=="__main__":
    s=Serializer()
    s.field('id',field_type=int)
    s.field('name',field_type=str)
    s.field('score',field_type=float,required=False,default=0.0)
    result=s.serialize({'id':1,'name':'Alice','score':95.5})
    assert result=={'id':1,'name':'Alice','score':95.5}
    result2=s.serialize({'id':2,'name':'Bob'})
    assert result2['score']==0.0
    deserialized=s.deserialize({'id':'3','name':'Charlie','score':'88'})
    assert deserialized=={'id':3,'name':'Charlie','score':88.0}
    print(f"Serialized: {result}")
    print("All tests passed!")
