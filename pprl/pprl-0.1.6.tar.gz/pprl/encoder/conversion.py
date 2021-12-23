from typing import List, Dict

from .model import AttributeValuePair, Entity, EncoderRequest, AttributeSchema, EncoderConfig, EncodedEntity


def serialize_attribute_value_pair(pair: AttributeValuePair) -> Dict:
    """
    Converts an attribute value pair into a dictionary:

    :param pair: Attribute value pair to convert
    :return: Converted attribute value pair
    """
    d = {
        "name": pair.name,
        "value": pair.value_as_string()
    }

    return d


def serialize_attribute_value_pairs(pair_list: List[AttributeValuePair]) -> List[Dict]:
    """
    Converts a list of attribute value pairs into a list of dictionaries.

    :param pair_list: List of attribute value pairs to convert
    :return: List of converted attribute value pairs
    """
    return [
        serialize_attribute_value_pair(pair) for pair in pair_list
    ]


def serialize_entity(entity: Entity) -> Dict:
    """
    Converts an entity into a dictionary.

    :param entity: Entity to convert
    :return: Converted entity
    """
    return {
        "identifier": entity.identifier,
        "attribute-value-list": serialize_attribute_value_pairs(entity.attributes)
    }


def serialize_entities(entity_list: List[Entity]) -> List[Dict]:
    """
    Converts an list of entities into a list of dictionaries.

    :param entity_list: Entities to convert
    :return: List of converted entities
    """
    return [
        serialize_entity(entity) for entity in entity_list
    ]


def serialize_schema(schema: AttributeSchema) -> Dict:
    """
    Converts an attribute schema into a dictionary.

    :param schema: Attribute schema to convert
    :return: Converted attribute schema
    """
    d = {"attribute-name": schema.attribute_name}
    d.update({
        k: str(v) for k, v in schema.options.items()
    })

    return d


def serialize_schemas(schema_list: List[AttributeSchema]) -> List[Dict]:
    """
    Converts a list of attribute schemas into a dictionary.

    :param schema_list: Attribute schemas to convert
    :return: List of converted attribute schemas
    """
    return [
        serialize_schema(schema) for schema in schema_list
    ]


def serialize_encoder_config(config: EncoderConfig) -> Dict:
    """
    Converts an encoder configuration object into a dictionary.

    :param config: Encoder configuration to convert
    :return: Converted encoder configuration
    """
    return {
        "charset": config.charset,
        "seed": config.seed,
        "generation-function": config.generation_function
    }


def serialize_encoder_request(request: EncoderRequest) -> Dict:
    """
    Converts an encoder request object into a dictionary.

    :param request: Encoder request to convert
    :return: Converted encoder request
    """
    if len(request.entity_list) == 0:
        return {}

    d = serialize_encoder_config(request.config)
    d["entity-list"] = serialize_entities(request.entity_list)
    d["schema-list"] = serialize_schemas(list(request.schema_list))

    return d


def deserialize_encoded_entity(d: Dict) -> EncodedEntity:
    """
    Converts a dictionary into an encoded entity.

    :param d: Dictionary to convert
    :return: Converted dictionary
    """
    return EncodedEntity(d["identifier"], d["encoding"])
