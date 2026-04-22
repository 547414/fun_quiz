from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from basic.minio_client.minio_client import MinioClient
from basic.redis_client.redis_client import RedisClient
from basic.repository.unit_of_work import UnitOfWork
from basic_module.repository.backend_api_repository import BackendApiRepository
from basic_module.repository.config_dict_repository import ConfigDictRepository
from basic_module.repository.dept_repository import DeptRepository
from basic_module.repository.file_info_repository import FileInfoRepository
from basic_module.repository.file_resource_repository import FileResourceRepository
from basic_module.repository.file_storage_repository import FileStorageRepository
from basic_module.repository.invite_code_repository import InviteCodeRepository
from basic_module.repository.menu_repository import MenuRepository
from basic_module.repository.organization_repository import OrganizationRepository
from basic_module.repository.permission_assign_repository import PermissionAssignRepository
from basic_module.repository.permission_repository import PermissionRepository
from basic_module.repository.role_repository import RoleRepository
from basic_module.repository.union_user_repository import UnionUserRepository
from basic_module.repository.union_user_user_repository import UnionUserUserRepository
from basic_module.repository.user_role_repository import UserRoleRepository
from basic_module.repository.web_user_organization_repository import WebUserOrganizationRepository
from basic_module.repository.web_user_dept_repository import WebUserDeptRepository
from basic_module.repository.web_user_repository import WebUserRepository
from basic_module.service.backend_api_service import BackendApiService
from basic_module.service.captcha_service import CaptchaService
from basic_module.service.check_permission_service import CheckPermissionService
from basic_module.service.config_dict_service import ConfigDictService
from basic_module.service.dept_service import DeptService
from basic_module.service.invite_code_service import InviteCodeService
from basic_module.service.menu_service import MenuService
from basic_module.service.organization_service import OrganizationService
from basic_module.service.permission_assign_service import PermissionAssignService
from basic_module.service.permission_service import PermissionService
from basic_module.service.role_service import RoleService
from basic_module.service.storage_service import StorageService
from basic_module.service.tools_service import ToolsService
from basic_module.service.tree_service import TreeService
from basic_module.service.union_user_service import UnionUserService
from basic_module.service.union_user_user_service import UnionUserUserService
from basic_module.service.web_user_organization_service import WebUserOrganizationService
from basic_module.service.user_role_service import UserRoleService
from basic_module.service.verification_code_service import VerificationCodeService
from basic_module.service.web_user_dept_service import WebUserDeptService
from basic_module.service.web_user_service import WebUserService


class BasicModuleContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html
    engine = providers.Singleton(
        create_engine,
        url=config.SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        pool_recycle=1800,
    )
    Session = providers.ThreadLocalSingleton(sessionmaker, bind=engine)
    session = providers.Singleton(scoped_session, Session)

    # Minio 客户端配置
    minio_client = providers.Singleton(
        MinioClient,
        config=config
    )

    # Redis 客户端配置
    redis_client = providers.Singleton(
        RedisClient,
        config=config
    )

    # 配置 UnitOfWork
    unit_of_work = providers.Factory(UnitOfWork, session_factory=session)

    organization_repository = providers.Factory(
        OrganizationRepository,
        session=session,
    )

    dept_repository = providers.Factory(
        DeptRepository,
        session=session,
    )

    file_info_repository = providers.Factory(
        FileInfoRepository,
        session=session,
    )

    file_storage_repository = providers.Factory(
        FileStorageRepository,
        session=session,
    )

    file_resource_repository = providers.Factory(
        FileResourceRepository,
        session=session,
    )

    web_user_repository = providers.Factory(
        WebUserRepository,
        session=session,
    )

    role_repository = providers.Factory(
        RoleRepository,
        session=session,
    )

    user_role_repository = providers.Factory(
        UserRoleRepository,
        session=session,
    )

    menu_repository = providers.Factory(
        MenuRepository,
        session=session,
    )

    permission_repository = providers.Factory(
        PermissionRepository,
        session=session,
    )

    permission_assign_repository = providers.Factory(
        PermissionAssignRepository,
        session=session,
    )

    backend_api_repository = providers.Factory(
        BackendApiRepository,
        session=session,
    )

    config_dict_repository = providers.Factory(
        ConfigDictRepository,
        session=session,
    )

    check_permission_service = providers.Factory(
        CheckPermissionService,
        web_user_repository=web_user_repository,
    )

    union_user_repository = providers.Factory(
        UnionUserRepository,
        session=session,
    )

    union_user_user_repository = providers.Factory(
        UnionUserUserRepository,
        session=session,
    )

    invite_code_repository = providers.Factory(
        InviteCodeRepository,
        session=session,
    )

    web_user_organization_repository = providers.Factory(
        WebUserOrganizationRepository,
        session=session,
    )

    web_user_dept_repository = providers.Factory(
        WebUserDeptRepository,
        session=session,
    )

    tools_service = providers.Factory(
        ToolsService,
    )

    tree_service = providers.Factory(
        TreeService,
    )

    organization_service = providers.Factory(
        OrganizationService,
        organization_repository=organization_repository,
        tree_service=tree_service,
    )

    dept_service = providers.Factory(
        DeptService,
        dept_repository=dept_repository,
        tree_service=tree_service,
    )

    user_role_service = providers.Factory(
        UserRoleService,
        user_role_repository=user_role_repository,
        role_repository=role_repository,
    )

    union_user_user_service = providers.Factory(
        UnionUserUserService,
        union_user_user_repository=union_user_user_repository,
        user_role_service=user_role_service,
        web_user_repository=web_user_repository,
    )

    invite_code_service = providers.Factory(
        InviteCodeService,
        invite_code_repository=invite_code_repository,
    )

    web_user_organization_service = providers.Factory(
        WebUserOrganizationService,
        web_user_organization_repository=web_user_organization_repository,
        organization_repository=organization_repository,
    )

    web_user_dept_service = providers.Factory(
        WebUserDeptService,
        web_user_dept_repository=web_user_dept_repository,
        dept_repository=dept_repository,
        organization_repository=organization_repository,
    )

    web_user_service = providers.Factory(
        WebUserService,
        web_user_repository=web_user_repository,
        redis_client=redis_client,
        user_role_service=user_role_service,
        minio_client=minio_client,
        backend_api_repository=backend_api_repository,
        union_user_user_service=union_user_user_service,
        union_user_repository=union_user_repository,
        union_user_user_repository=union_user_user_repository,
        role_repository=role_repository,
        user_role_repository=user_role_repository,
        organization_repository=organization_repository,
        web_user_organization_repository=web_user_organization_repository,
        web_user_dept_repository=web_user_dept_repository,
        dept_repository=dept_repository,
        invite_code_service=invite_code_service,
        tools_service=tools_service,
        web_user_organization_service=web_user_organization_service,
        web_user_dept_service=web_user_dept_service,
    )

    union_user_service = providers.Factory(
        UnionUserService,
        union_user_repository=union_user_repository,
        backend_api_repository=backend_api_repository,
        union_user_user_service=union_user_user_service,
        web_user_service=web_user_service,
        minio_client=minio_client,
        redis_client=redis_client,
    )

    storage_service = providers.Factory(
        StorageService,
        minio_client=minio_client,
        file_info_repository=file_info_repository,
        file_storage_repository=file_storage_repository,
        file_resource_repository=file_resource_repository,
        # auth_service=auth_service
    )

    role_service = providers.Factory(
        RoleService,
        role_repository=role_repository,
    )

    menu_service = providers.Factory(
        MenuService,
        menu_repository=menu_repository,
        tree_service=tree_service,
        check_permission_service=check_permission_service,
    )

    backend_api_service = providers.Factory(
        BackendApiService,
        backend_api_repository=backend_api_repository,
    )

    permission_assign_service = providers.Factory(
        PermissionAssignService,
        permission_assign_repository=permission_assign_repository,
    )

    permission_service = providers.Factory(
        PermissionService,
        permission_repository=permission_repository,
        permission_assign_service=permission_assign_service,
        menu_repository=menu_repository,
        backend_api_repository=backend_api_repository,
    )

    verification_code_service = providers.Factory(
        VerificationCodeService,
    )

    config_dict_service = providers.Factory(
        ConfigDictService,
        config_dict_repository=config_dict_repository,
    )

    captcha_service = providers.Factory(
        CaptchaService,
        redis_client=redis_client,
    )
