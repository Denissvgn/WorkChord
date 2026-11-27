# RoutingCalibrationContractService__validated_terms

**Entry point:** `routing_calibration_contract_service.RoutingCalibrationContractService._validated_terms`
**Modules involved:** [agent_routing_policy](../modules/agent_routing_policy.md), [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md), [routing_qualification_key_service](../modules/routing_qualification_key_service.md), [time](../modules/time.md)

> Refuse unknown or retired keys and a bias review dated in the future.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `routing_qualification_key_service.require_known_qualification_keys`
2. `time.utc_now`
3. `agent_routing_policy.RoutingTermsRefusedError`

## Touches

- [agent_routing_policy](../modules/agent_routing_policy.md)
- [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md)
- [routing_qualification_key_service](../modules/routing_qualification_key_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `routing_calibration_contract_service.RoutingCalibrationContractService._validated_terms`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
