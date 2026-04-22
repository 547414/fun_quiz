from typing import List

from basic_module.model.menu_model import EditMenuModel, SaveMenuSeqAndParentModel, MenuTreeViewModel, \
    MenuTreeParamsModel, DeleteMenuParamsModel, MenuPageParamsModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.repository.menu_repository import MenuRepository
from basic_module.service.check_permission_service import CheckPermissionService
from basic_module.service.tree_service import TreeService


class MenuService:
    def __init__(
            self,
            menu_repository: MenuRepository,
            tree_service: TreeService,
            check_permission_service: CheckPermissionService
    ):
        self.__menu_repository = menu_repository
        self.__tree_service = tree_service
        self.__check_permission_service = check_permission_service

    def get_menu_tree(
            self,
            params: MenuTreeParamsModel,
    ):
        tree_list = self.__menu_repository.get_menu_tree(
            params=params,
        )
        for tree in tree_list:
            tree.type_display = str(tree.type)
        tree_data = tree_list
        if len(tree_list) > 1:
            tree_data = self.__tree_service.build_tree(tree_list)
        if len(tree_list) == 1:
            tree_data[0].children = []
        return tree_data

    def get_allow_menu_tree(
            self,
            params: MenuTreeParamsModel,
            current_user_info: ValidateTokenResModel
    ):
        tree_list = self.__menu_repository.get_allow_menu_tree(
            params=params,
            current_user_info=current_user_info
        )
        for tree in tree_list:
            tree.type_display = str(tree.type)
        tree_data = tree_list
        if len(tree_list) > 1:
            tree_data = self.__tree_service.build_tree(tree_list)
        if len(tree_list) == 1:
            tree_data[0].children = []
        return tree_data

    def edit_menu(
            self,
            params: EditMenuModel,
    ):
        if params.id:
            menu = self.__menu_repository.get_by_id(
                menu_id=params.id
            )
            menu.name = params.name
            menu.code = params.code
            menu.enabled = params.enabled
            menu.parent_id = params.parent_id
            menu.url = params.url
            menu.icon = params.icon
            menu.seq = params.seq
            menu.type = params.type
            self.__menu_repository.update(
                model=menu
            )
        else:
            max_seq_model = self.__menu_repository.get_max_seq(
                parent_id=params.parent_id
            )
            if max_seq_model:
                params.seq = max_seq_model.max_seq + 1
            else:
                params.seq = 0
            self.__menu_repository.insert(
                model=params.to_menu_model()
            )
        return True

    def get_menu_detail(
            self,
            menu_id: str,
    ):
        return self.__menu_repository.get_menu_detail(
            menu_id=menu_id
        )

    def delete_menu(
            self,
            params: DeleteMenuParamsModel,
    ):
        self.__menu_repository.delete_by_id(
            menu_id=params.menu_id
        )

    def save_seq_and_parent(
            self,
            params: SaveMenuSeqAndParentModel,
    ):
        self.do_save_seq_and_parent(
            menu_list=params.menu_tree
        )

    def do_save_seq_and_parent(
            self,
            menu_list: List[MenuTreeViewModel]
    ):
        for index, menu in enumerate(menu_list):
            menu_model = self.__menu_repository.get_by_id(
                menu_id=menu.id
            )
            menu_model.seq = menu.seq
            menu_model.parent_id = menu.parent_id
            self.__menu_repository.update(
                model=menu_model
            )
            if menu.children:
                self.do_save_seq_and_parent(
                    menu_list=menu.children
                )
        return True

    def get_menu_page(
            self,
            params: MenuPageParamsModel,
    ):
        return self.__menu_repository.get_menu_page(
            params=params
        )
