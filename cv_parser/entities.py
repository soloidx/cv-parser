import collections
import logging
from typing import Dict, List


class CVParsedException(Exception):
    pass


class CVParsedFormationException(Exception):
    pass


class PersonalInfo:
    def __init__(self, personal_info: Dict) -> None:
        try:
            # TODO: define which fields could be optional
            self.first_name = personal_info["first_name"]
            self.last_name = personal_info["last_name"]
            self.title = personal_info["title"]
            self.headline = personal_info["headline"]
            self.address = personal_info["address"]
            self.phone = personal_info["phone"]
            self.email = personal_info["email"]
            self.webpage = personal_info["webpage"]
            self.picture = personal_info["picture"]
        except KeyError as e:
            raise CVParsedException(
                "Cannot parse fields from personal_info: "
            ) from e


CoreFormationItem = collections.namedtuple(
    "CoreFormationItem", ["title", "date", "institution", "location"]
)


class CoreFormation:
    def __init__(self, core_formation: List) -> None:
        self.core_formation = []
        for cf in core_formation:
            try:
                item = CoreFormationItem(
                    title=cf["title"],
                    date=cf["date"],
                    institution=cf["institution"],
                    location=cf["location"],
                )
                self.core_formation.append(item)
            except KeyError as e:
                logging.warning(
                    CVParsedFormationException(
                        "Cannot parse fields from personal_info: %s" % e
                    )
                )
