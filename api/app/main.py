from fastapi.middleware.cors import CORSMiddleware
from ipaddress import IPv4Address, IPv4Network
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
import geoip2.database
import re
import redis


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REDIS_HOST = environ.get('REDIS_HOST', '127.0.0.1')
# rd = redis.Redis(host=REDIS_HOST, port=6379, db=0)

class MyIPv4(IPv4Address):
    @property
    def binary_repr(self, sep=".") -> str:
        """Represent IPv4 as 4 blocks of 8 bits."""
        return sep.join(f"{i:08b}" for i in self.packed)

    @classmethod
    def from_binary_repr(cls, binary_repr: str):
        """Construct IPv4 from binary representation."""
        # Remove anything that's not a 0 or 1
        i = int(re.sub(r"[^01]", "", binary_repr), 2)
        return cls(i)


@app.get("/", summary="Hello World")
def read_root():
    return JSONResponse(content={"msg": "I'm IpFast"})


@app.get("/ip_lookup/")
def ip_lookup(ip: str):
    try:
        net = IPv4Network(ip, False)
    except Exception as e:
        print(e)
        # raise HTTPException(status_code=503, detail="Environ exception")
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={'msg': 'NOT ACCEPTABLE'})


    with geoip2.database.Reader('./GeoLite2-City.mmdb') as reader:
        response = reader.city(str(net.network_address))

        data = {
            "country": response.country.name,
            "city": response.city.name,
            "address": str(net),
            "netmask": str(net.netmask),
            "network_address": str(net.network_address),
            "broadcast_address": str(net.broadcast_address),
            "binary_repr": str(MyIPv4(str(net.network_address)).binary_repr),
            "prefixlen": str(net.prefixlen),
            "version": str(net.version),
            "host_min": str(net[0]),
            "host_max": str(net[-1]),
            "num_addresses": str(net.num_addresses),
        }
        # cache = rd.get(instance)
        # rd.set(instance, json.dumps(result_rows))
        # rd.expire(instance, 300)

        return JSONResponse(content={'msg': data})
