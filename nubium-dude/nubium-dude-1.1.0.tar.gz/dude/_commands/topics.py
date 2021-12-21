import json
import importlib
import click
from . import dude_cli
from nubium_utils.confluent_utils import KafkaToolbox
from nubium_schemas.nubium_shared_apps.eloqua import eloqua_retriever_timestamp


def _must_be_a_valid_nubium_schema_import(ctx, param, value):
    if value is not None:
        try:
            components = value.split(".")
            module = importlib.import_module(".".join(["nubium_schemas"] + components[0:-1]))
            return getattr(module, components[-1])
        except ImportError as exc:
            raise click.BadParameter(
                ctx=ctx, param=param, message=f'"{value}" is not a valid python attribute to import'
            ) from exc
    return value


def _require_schema_file_when_schema_not_prestent(ctx, param, value):
    if value is None and ctx.params["schema"] is None:
        raise click.MissingParameter(ctx=ctx, param=param, message="Required if --schema not present")
    return value


@dude_cli.group("topics")
@click.pass_context
@click.option("--bootstrap-servers")
@click.option("--rhosak-username")
@click.option("--rhosak-password")
@click.option("--security-protocol")
@click.option("--sasl-mechanisms")
def topics_group(ctx, bootstrap_servers, rhosak_username, rhosak_password, security_protocol, sasl_mechanisms):
    ctx.obj = KafkaToolbox(
        config={
            k: v
            for k, v in {
                "bootstrap.servers": bootstrap_servers,
                "sasl.username": rhosak_username,
                "sasl.password": rhosak_password,
                "security.protocol": security_protocol,
                "sasl.mechanisms": sasl_mechanisms,
            }.items()
            if v
        }
    )


pass_kafka_toolbox = click.make_pass_decorator(KafkaToolbox)


@pass_kafka_toolbox
def create_all_topics(kafka_toolbox, ctx, param, value):
    kafka_toolbox.create_all_topics()
    ctx.exit()


@topics_group.command(name="create")
@pass_kafka_toolbox
@click.option("--all", is_flag=True, expose_value=False, is_eager=True, callback=create_all_topics)
@click.option("--topics", type=str, required=True)
@click.option("--num-partitions", type=int, default=3)
@click.option("--replication-factor", type=int, default=3)
@click.option("--ignore-cluster-maps", is_flag=True)
@click.option("--topic-config", type=dict, default={})
def create_topics(kafka_toolbox, topics, num_partitions, replication_factor, ignore_cluster_maps, topic_config):
    kafka_toolbox.create_topics(
        {topic: "" for topic in topics.split(",")},
        num_partitions=num_partitions,
        replication_factor=replication_factor,
        ignore_nubium_topic_cluster_maps=ignore_cluster_maps,
        topic_config=topic_config,
    )


@topics_group.command(name="delete")
@pass_kafka_toolbox
@click.option("--topics", type=str, required=True)
@click.option("--ignore-cluster-maps", is_flag=True)
def delete_topics(kafka_toolbox, topics, ignore_cluster_maps):
    kafka_toolbox.delete_topics(
        {topic: "" for topic in topics.split(",")},
        ignore_nubium_topic_cluster_maps=ignore_cluster_maps,
    )


@topics_group.command(name="list")
@pass_kafka_toolbox
@click.option("--by-topic", type=bool, default=False)
@click.option("--all-clusters", type=bool, default=True)
@click.option("--mirrors", type=bool, default=False)
@click.option("--cluster", type=str, default="")
def list_topics(kafka_toolbox, by_topic, all_clusters, mirrors, cluster):
    click.echo(
        json.dumps(
            kafka_toolbox.list_topics(
                by_topic=by_topic,
                all_clusters=all_clusters,
                mirrors=mirrors,
                cluster=cluster,
            ),
            indent=4,
        )
    )


@topics_group.command(name="produce")
@pass_kafka_toolbox
@click.option("--topic", required=True)
@click.option("--message-file", required=True, type=click.File("r"))
@click.option(
    "--schema",
    callback=_must_be_a_valid_nubium_schema_import,
    help="Path to import schema from nubium_schemas Ex: people_stream.person_schema",
)
def produce_message(kafka_toolbox, topic, message_file, schema):
    messages = json.loads(message_file.read())
    kafka_toolbox.produce_messages(
        topic=topic,
        message_list=messages,
        schema=schema,
    )


def format_message(message):
    return {
            "headers": {key: value.decode("utf-8")  for key, value in dict(message.headers()).items()},
            "key": message.key(),
            "value": message.value(),
        }


@topics_group.command(name="consume")
@pass_kafka_toolbox
@click.option("--topic", required=True)
@click.option("--message-file", required=True, type=click.File("w"))
def consume_message(kafka_toolbox, topic, message_file):
    messages = kafka_toolbox.consume_messages(
        topic=topic,
    )
    json.dump([format_message(message) for message in messages] if messages else [], message_file, indent=4, sort_keys=True)


@topics_group.command(name="timestamp")
@pass_kafka_toolbox
@click.option("--topic", required=True)
@click.option("--time", required=True)
def produce_timestamp(kafka_toolbox, topic, time):
    kafka_toolbox.produce_messages(
        topic=topic,
        schema=eloqua_retriever_timestamp,
        message_list=[dict(
            headers={
                "guid": "N/A",
                "last_updated_by": "dude"
            },
            key='dude_timestamp',
            value={"timestamp": time}
            )
        ],
    )

# @topics_group.command(name="wipe")
# @pass_kafka_toolbox
# @click.option("--topic", required=True)
# def wipe_topic(kafka_toolbox, topic):
#     kafka_toolbox.wipe_topic(topic)
