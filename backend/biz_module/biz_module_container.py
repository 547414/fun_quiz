from dependency_injector import containers, providers

from basic_module.basic_module_container import BasicModuleContainer
from biz_module.repository.quiz_repository import QuizRepository
from biz_module.repository.quiz_question_repository import QuizQuestionRepository
from biz_module.repository.quiz_outcome_repository import QuizOutcomeRepository
from biz_module.repository.quiz_token_repository import QuizTokenRepository
from biz_module.repository.quiz_token_quiz_repository import QuizTokenQuizRepository
from biz_module.repository.quiz_result_repository import QuizResultRepository
from biz_module.service.quiz_service import QuizService
from biz_module.service.quiz_token_service import QuizTokenService
from biz_module.service.quiz_play_service import QuizPlayService
from biz_module.service.quiz_stats_service import QuizStatsService


class BizModuleContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    basic_module_container = providers.Container(BasicModuleContainer)

    session = basic_module_container.session
    minio_client = basic_module_container.minio_client
    unit_of_work = basic_module_container.unit_of_work

    # Repositories
    quiz_repository = providers.Factory(
        QuizRepository,
        session=session,
    )

    quiz_question_repository = providers.Factory(
        QuizQuestionRepository,
        session=session,
    )

    quiz_outcome_repository = providers.Factory(
        QuizOutcomeRepository,
        session=session,
    )

    quiz_token_repository = providers.Factory(
        QuizTokenRepository,
        session=session,
    )

    quiz_token_quiz_repository = providers.Factory(
        QuizTokenQuizRepository,
        session=session,
    )

    quiz_result_repository = providers.Factory(
        QuizResultRepository,
        session=session,
    )

    # Services
    quiz_token_service = providers.Factory(
        QuizTokenService,
        quiz_token_repository=quiz_token_repository,
        quiz_token_quiz_repository=quiz_token_quiz_repository,
    )

    quiz_service = providers.Factory(
        QuizService,
        quiz_repository=quiz_repository,
        quiz_question_repository=quiz_question_repository,
        quiz_outcome_repository=quiz_outcome_repository,
        minio_client=minio_client,
    )

    quiz_play_service = providers.Factory(
        QuizPlayService,
        quiz_repository=quiz_repository,
        quiz_question_repository=quiz_question_repository,
        quiz_outcome_repository=quiz_outcome_repository,
        quiz_result_repository=quiz_result_repository,
        quiz_token_service=quiz_token_service,
        minio_client=minio_client,
    )

    quiz_stats_service = providers.Factory(
        QuizStatsService,
        quiz_repository=quiz_repository,
        quiz_result_repository=quiz_result_repository,
    )
