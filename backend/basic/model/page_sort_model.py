from enum import Enum


class EnumPageSortModel(Enum):
    ASC = 'ASC'
    DESC = 'DESC'

    def __str__(self):
        labels = {
            EnumPageSortModel.ASC: "升序",
            EnumPageSortModel.DESC: "降序",
        }
        return labels[self]
