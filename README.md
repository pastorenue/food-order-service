# Food-Order-Service Development
The development environment can be started using Docker and Docker compose
tools. The docker-compose will create a container named `backend-api`

### Environment and setup
Set up the following environment variables:
export BASE_API_URL="https://nourish.me/api"
export CLIENT_API_KEY="CLIENT_API_KEY"
export ENVIRONMENT=(prod or stage) default is "dev"

#### Build image

The first time you start the environment you will need some extra steps. First
of them is creating the docker image.
```
$ cd food_order_system
$ docker-compose build
```
#### How it works
The main goal of the service to convert xml files to json format and process the data
to be compatible with what the nourish.me API accepts. To test only the part that does
this functionality, you can just use the functions from the `util module`
```
>>> from backend_api.utils import _xml_to_dict, format_order_request_body
```
You can pass in an xml object into either of the functions to get a dictionary.
The major difference between the `_xml_to_dict` and `format_order_request_body` function
is that the `_xml_to_dict` function serves as a helper function to the `format_order_request_body`
function which does the formatting.

```
>>> xml = '''
<notes>
    <note>
        <type>Short</type>
        <description>...</description>
    </note>
</notes>
'''
>>> dict_obj = _xml_to_dict(xml)
{"notes": {"note": [{"type": "Short", "description": "..."}]}}
```

The `format_order_request_body` function is more tailored to a specific xml
structure: `Employee XML` file while the _`xml_to_dict` is generic

#### Tests
To run tests, you can do that from the docker shell
```
$ docker-compose run --rm backend-api sh
$ pytest
```

