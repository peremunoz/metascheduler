from api.constants.cluster_mode import ClusterMode
from api.daemons.policies.implementations.best_effort import BestEffortPolicy
from api.daemons.policies.implementations.dynamic import DynamicPolicy
from api.daemons.policies.implementations.exclusive import ExclusivePolicy
from api.daemons.policies.implementations.shared import SharedPolicy
from api.daemons.policies.planification_policy import PlanificationPolicy


def get_policy_by_name(policy_name: ClusterMode, policy: PlanificationPolicy) -> PlanificationPolicy:
    '''
    Gets the policy class based on the policy name.

    '''
    if policy_name.value == ClusterMode.EXCLUSIVE.value:
        return ExclusivePolicy(policy)
    if policy_name.name == ClusterMode.BEST_EFFORT.value:
        return BestEffortPolicy(policy)
    if policy_name.name == ClusterMode.SHARED.value:
        return SharedPolicy(policy)
    if policy_name.name == ClusterMode.DYNAMIC.value:
        return DynamicPolicy(policy)
    else:
        raise ValueError('Policy not implemented')
