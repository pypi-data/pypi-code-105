from typing import List, Dict

import datahub.emitter.mce_builder as builder
import datahub.metadata.schema_classes as models

from dh_client.entities import Entity
from dh_client.entities.custom_properties import CustomProperty
from dh_client.entities.glossary_terms import GlossaryTerm
from dh_client.entities.owners import Owner
from dh_client.entities.tags import Tag
from dh_client.entities.links import Link


class Dataset(Entity):
    """
    Examples:

        The standard way:

        >>> client.dataset.upsert(name="projectA.datasetB.tableC", description="A random dataset description",
        ...                       tags=["foo"], owners=["team1@domain.com", "user2@domain.com"],
        ...                       glossary_terms=["gloss_term1"], upstream_datasets=["projectA.datasetB.tableD"],
        ...                       links={"Kaggle": "https://kaggle.com/randomuser/randomdataset"},
        ...                       custom_properties={'a': 'b'}
        ... )

        Modify dataset using a JSON file:

        $ ls *.json
        dataset_definitions.json
        $ cat dataset_definitions.json
        {"name": "projectA.datasetB.tableC", "description": "A random dataset description"}
        >>> client.dataset.upsert(file_pattern="*.json")
    """

    entity_type: str = "dataset"
    aspect_name: str = "datasetProperties"

    def _create_mpc(
        self,
        name: str,
        platform: str = "bigquery",
        env: str = "DEV",
        description: str = None,
        url: str = None,
        tags: List[str] = None,
        owners: List[str] = None,
        custom_properties=None,
        glossary_terms: List[str] = None,
        upstream_datasets: List[str] = None,
        links: dict = None,
    ) -> List[dict]:
        dataset_urn: str = builder.make_dataset_urn(
            platform=platform, name=name, env=env
        )
        """Create list of mpc dictionaries for dataset modifications.
        
        Args:
            name: The dataset name.
            platform: The platform name.
            env: The environment.
            description: The dataset's description.
            url: Dataset's url.
            tags: List of tags.
            owners: List of owners.
            custom_properties: Key/value custom properties.
            glossary_terms: List of glossary terms.
            upstream_datasets: List of upstream datasets.
        
        Returns:
            a list of mpc dictionaries.
        """

        mpc = [
            dict(
                entityType=Dataset.entity_type,
                entityUrn=dataset_urn,
                aspectName=Dataset.aspect_name,
                aspect=models.DatasetPropertiesClass(
                    description=description, externalUrl=url
                ),
            )
        ]

        if tags:
            mpc.append(Tag.create_mpc_association(self.entity_type, dataset_urn, tags))
        if owners:
            mpc.append(
                Owner.create_mpc_association(self.entity_type, dataset_urn, owners)
            )
        if custom_properties:
            mpc.append(
                CustomProperty.create_mpc_association(
                    self.entity_type, dataset_urn, custom_properties
                )
            )
        if glossary_terms:
            mpc.append(
                GlossaryTerm.create_mpc_association(
                    self.entity_type,
                    dataset_urn,
                    glossary_terms,
                    self.emmiter.datahub_actor,
                )
            )
        if upstream_datasets:
            mpc.append(
                self.create_mpc_upstream_association(
                    dataset_urn, upstream_datasets, self.emmiter.dataset_platform
                )
            )
        if links:
            mpc.append(
                Link.create_mpc_association(
                    self.entity_type, dataset_urn, links, self.emmiter.datahub_actor
                )
            )

        return mpc

    def create_mpc_upstream_association(
        self,
        dataset_urn: str,
        upstream_datasets: List[str],
        platform: str,
    ) -> dict:
        """Associate a list of upstream datasets with the given dataset.

        Args:
            dataset_urn: The dataset URN.
            upstream_datasets: List of upstream datasets.
            platform: The dataset platform.

        Returns:
            A list with a single mpc dictionary.
        """
        return self._create_mpc_dict(
            self.entity_type,
            dataset_urn,
            "upstreamLineage",
            models.UpstreamLineageClass(
                upstreams=[
                    models.UpstreamClass(
                        dataset=self._create_resource_urn(
                            upstream_dataset, platform, self.emmiter.env
                        ),
                        type=models.DatasetLineageTypeClass.TRANSFORMED,
                    )
                    for upstream_dataset in upstream_datasets
                ]
            ),
        )

    def delete_tag(self, dataset_urn: str, tag: str) -> None:
        """Delete tag from a dataset TODO: debug this

        Examples:

            >>> client.dataset.delete_tag("projectA.datasetB.tableC", "foo")
        """
        body = {
            "query": "mutation removeTag($input: TagAssociationInput!) {removeTag(input: $input)}",
            "variables": {
                "input": {
                    "tagUrn": builder.make_tag_urn(tag),
                    "resourceUrn": self._create_resource_urn(dataset_urn),
                }
            },
        }
        self._apply_mcp(None, [body], use_graphql=True)

    @staticmethod
    def _create_resource_urn(dataset: str, platform, env) -> str:
        """Create the dataset urn using emitters' attributes.

        Args:
            dataset: dataset name

        Returns:
            The dataset URN.
        """
        return builder.make_dataset_urn(platform, dataset, env)
