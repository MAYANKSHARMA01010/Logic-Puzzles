from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from models import (
    Domain,
    ForecastAuditAction,
    ForecastAuditObservation,
    ForecastAuditState,
    Operation,
    RewardModel,
    Severity,
)


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    difficulty: str
    domain: Domain
    metric_name: str
    timestamps: List[str]
    values: List[Optional[float]]
    issue_type: str
    constraints: List[str]
    analyst_note: str
    history_summary: str
    max_steps: int
    expected_operation: Operation
    expected_index: Optional[int]
    expected_value: Optional[float]
    expected_severity: Optional[Severity]
    expected_constraints: List[str]
    value_tolerance: float


TASKS: List[TaskSpec] = [
    TaskSpec(
        task_id="easy_ops_missing_001",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="warehouse_orders_per_hour",
        timestamps=["09:00", "10:00", "11:00", "12:00", "13:00"],
        values=[120.0, 125.0, 130.0, None, 140.0],
        issue_type="missing_value",
        constraints=[
            "Weekday ramp is stable at +5 orders/hour.",
            "No promotions or outages were recorded.",
        ],
        analyst_note="Backfill the missing hour before the report is published.",
        history_summary="Recent weekday mornings have shown a steady linear ramp.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=3,
        expected_value=135.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.25,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_001",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_strategy_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[101.0, 103.0, 104.0, 980.0, 106.0],
        issue_type="anomaly",
        constraints=[
            "Historical daily P&L usually changes by less than 5k day-to-day.",
            "No major event, rebalance, or macro release occurred on Thu.",
        ],
        analyst_note="Decide whether Thursday should be accepted, repaired, or escalated.",
        history_summary="The desk has been running low-volatility market-neutral intraday strategies.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=105.0,
        expected_severity=Severity.high,
        expected_constraints=["Historical daily P&L usually changes by less than 5k day-to-day."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_001",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_grid_demand_forecast_mw",
        timestamps=["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
        values=[950.0, 990.0, 1030.0, 1205.0, 1110.0, 1080.0],
        issue_type="invalid_forecast",
        constraints=[
            "Peak-hour demand should rise smoothly by about 30-50 MW/hour from 18:00 to 21:00.",
            "At 21:00, forecast demand must stay below 1100 MW because feeder maintenance limits transfer capacity.",
            "After the peak, demand should decline, not jump upward again.",
        ],
        analyst_note="Validate the forecast against physical and operational constraints.",
        history_summary="This is an evening peak forecast for a balancing area under a temporary transfer-cap limit.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=1080.0,
        expected_severity=Severity.high,
        expected_constraints=[
            "At 21:00, forecast demand must stay below 1100 MW because feeder maintenance limits transfer capacity.",
        ],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="easy_ops_missing_002",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="daily_ticket_volume",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[210.0, 215.0, None, 225.0, 230.0],
        issue_type="missing_value",
        constraints=[
            "Volume has been increasing by +5 tickets/day this week.",
            "No staffing or routing change happened on Wed.",
        ],
        analyst_note="Fill the missing day before closing the weekly report.",
        history_summary="Support demand is following a stable linear rise.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=2,
        expected_value=220.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.5,
    ),
    TaskSpec(
        task_id="easy_ops_missing_003",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="hourly_packaging_units",
        timestamps=["08:00", "09:00", "10:00", "11:00", "12:00"],
        values=[480.0, 500.0, 520.0, None, 560.0],
        issue_type="missing_value",
        constraints=[
            "Packaging line output rises by +20 units/hour in this shift.",
            "No downtime was reported at 11:00.",
        ],
        analyst_note="Backfill the missing hourly production point.",
        history_summary="Morning shift has a smooth, repeatable ramp profile.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=3,
        expected_value=540.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=1.0,
    ),
    TaskSpec(
        task_id="easy_ops_missing_004",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="daily_fulfillment_rate_pct",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[96.0, 96.5, None, 97.5, 98.0],
        issue_type="missing_value",
        constraints=[
            "Fulfillment has been improving by +0.5 percentage points/day.",
            "No policy change was introduced mid-week.",
        ],
        analyst_note="Complete the missing KPI value for Wednesday.",
        history_summary="Trend is a steady improvement throughout the week.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=2,
        expected_value=97.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.1,
    ),
    TaskSpec(
        task_id="easy_ops_missing_005",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="hourly_pick_rate_units",
        timestamps=["13:00", "14:00", "15:00", "16:00", "17:00"],
        values=[300.0, None, 320.0, 330.0, 340.0],
        issue_type="missing_value",
        constraints=[
            "Pick rate follows a +10 units/hour ramp in this interval.",
            "No picker reassignment occurred at 14:00.",
        ],
        analyst_note="Impute the missing 14:00 value.",
        history_summary="Observed values indicate a simple linear progression.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=1,
        expected_value=310.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.5,
    ),
    TaskSpec(
        task_id="easy_ops_missing_006",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="daily_returns_count",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[42.0, 44.0, 46.0, None, 50.0],
        issue_type="missing_value",
        constraints=[
            "Returns rose by +2 each day this week.",
            "No one-off incident occurred on Thu.",
        ],
        analyst_note="Backfill the missing daily returns point.",
        history_summary="Series is linear with constant daily increment.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=3,
        expected_value=48.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.25,
    ),
    TaskSpec(
        task_id="easy_ops_missing_007",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="hourly_dispatch_trucks",
        timestamps=["06:00", "07:00", "08:00", "09:00", "10:00"],
        values=[12.0, 13.0, None, 15.0, 16.0],
        issue_type="missing_value",
        constraints=[
            "Dispatch volume increases by one truck each hour.",
            "Fleet availability remained unchanged.",
        ],
        analyst_note="Estimate the missing 08:00 dispatch count.",
        history_summary="Morning dispatch pattern is a clean +1/hour line.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=2,
        expected_value=14.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.1,
    ),
    TaskSpec(
        task_id="easy_ops_missing_008",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="daily_on_time_shipments_pct",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[92.0, 92.4, 92.8, None, 93.6],
        issue_type="missing_value",
        constraints=[
            "On-time performance improved by +0.4 points/day.",
            "No weather or network disruption occurred on Thu.",
        ],
        analyst_note="Complete the missing on-time KPI.",
        history_summary="This week shows smooth incremental improvement.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=3,
        expected_value=93.2,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.1,
    ),
    TaskSpec(
        task_id="easy_ops_missing_009",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="hourly_loading_dock_utilization_pct",
        timestamps=["14:00", "15:00", "16:00", "17:00", "18:00"],
        values=[70.0, 72.0, 74.0, 76.0, None],
        issue_type="missing_value",
        constraints=[
            "Dock utilization rose by +2 points each hour.",
            "No shift handoff delay happened at 18:00.",
        ],
        analyst_note="Fill the final missing utilization point.",
        history_summary="Late-afternoon loading shows a linear increase.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=4,
        expected_value=78.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.25,
    ),
    TaskSpec(
        task_id="easy_ops_missing_010",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="daily_order_accuracy_pct",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[97.2, None, 97.6, 97.8, 98.0],
        issue_type="missing_value",
        constraints=[
            "Accuracy improved by +0.2 points/day this week.",
            "No audit procedure changed on Tue.",
        ],
        analyst_note="Recover the missing Tuesday accuracy metric.",
        history_summary="Quality trend is stable and monotonic.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=1,
        expected_value=97.4,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.1,
    ),
    TaskSpec(
        task_id="easy_ops_missing_011",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="hourly_inbound_pallets",
        timestamps=["05:00", "06:00", "07:00", "08:00", "09:00"],
        values=[50.0, 55.0, 60.0, None, 70.0],
        issue_type="missing_value",
        constraints=[
            "Inbound pallets increase by +5 each hour.",
            "No truck cancellation occurred at 08:00.",
        ],
        analyst_note="Backfill the missing inbound count.",
        history_summary="Inbound cadence is a deterministic linear ramp.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=3,
        expected_value=65.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.25,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_002",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_options_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[88.0, 90.0, 91.0, 460.0, 93.0],
        issue_type="anomaly",
        constraints=[
            "Desk P&L usually changes by less than 5k day-to-day.",
            "No macro event occurred on Thu.",
        ],
        analyst_note="Assess the Thursday spike and decide final action.",
        history_summary="Book has been low-vol and tightly mean-reverting.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=92.0,
        expected_severity=Severity.high,
        expected_constraints=["Desk P&L usually changes by less than 5k day-to-day."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_003",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_fx_strategy_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[120.0, 121.0, 122.0, 780.0, 123.0],
        issue_type="anomaly",
        constraints=[
            "Normal day-to-day drift is within +/-3k.",
            "No extraordinary FX move was recorded on Thu.",
        ],
        analyst_note="Determine if Thursday is corrupt and repair if needed.",
        history_summary="Strategy has stable risk and narrow daily variance.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=122.5,
        expected_severity=Severity.high,
        expected_constraints=["Normal day-to-day drift is within +/-3k."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_004",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_credit_book_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[75.0, 77.0, 78.0, 520.0, 80.0],
        issue_type="anomaly",
        constraints=[
            "Credit book P&L usually moves under 4k per day.",
            "No idiosyncratic spread shock happened on Thu.",
        ],
        analyst_note="Investigate the outlier and return a corrected point.",
        history_summary="Portfolio shows mild monotonic improvement.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=79.0,
        expected_severity=Severity.high,
        expected_constraints=["Credit book P&L usually moves under 4k per day."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_005",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_equities_alpha_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[132.0, 133.0, 134.0, 950.0, 136.0],
        issue_type="anomaly",
        constraints=[
            "Alpha sleeve typically changes by less than 4k/day.",
            "No earnings cluster arrived on Thu.",
        ],
        analyst_note="Handle the Thursday anomaly with a final repair action.",
        history_summary="Signal quality has been stable across the week.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=135.0,
        expected_severity=Severity.high,
        expected_constraints=["Alpha sleeve typically changes by less than 4k/day."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_006",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_rates_book_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[64.0, 65.0, 66.0, 410.0, 67.0],
        issue_type="anomaly",
        constraints=[
            "Rates desk variance is normally below 3k day-to-day.",
            "No central bank surprise was announced on Thu.",
        ],
        analyst_note="Evaluate the spike and produce corrected Thursday value.",
        history_summary="Rates book has a low-volatility profile this week.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=66.5,
        expected_severity=Severity.high,
        expected_constraints=["Rates desk variance is normally below 3k day-to-day."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_007",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_etf_arb_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[55.0, 56.0, 57.0, 390.0, 58.0],
        issue_type="anomaly",
        constraints=[
            "ETF arb P&L generally moves by less than 2k/day.",
            "No index rebalance occurred on Thu.",
        ],
        analyst_note="Repair the likely corrupted Thursday point.",
        history_summary="Strategy exhibits tight and stable daily distribution.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=57.5,
        expected_severity=Severity.high,
        expected_constraints=["ETF arb P&L generally moves by less than 2k/day."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_008",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_vol_surface_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[142.0, 143.0, 144.0, 860.0, 145.0],
        issue_type="anomaly",
        constraints=[
            "Vol-surface desk normally shifts under 4k/day.",
            "No event-vol shock took place on Thu.",
        ],
        analyst_note="Judge anomaly severity and return repaired value.",
        history_summary="PnL progression is near-linear outside the outlier.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=144.5,
        expected_severity=Severity.high,
        expected_constraints=["Vol-surface desk normally shifts under 4k/day."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_009",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_macro_basket_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[95.0, 96.0, 97.0, 610.0, 98.0],
        issue_type="anomaly",
        constraints=[
            "Macro basket daily move is usually below 3k.",
            "No major macro print happened on Thu.",
        ],
        analyst_note="Resolve the Thursday anomaly before publishing results.",
        history_summary="Risk regime has been calm and stationary.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=97.5,
        expected_severity=Severity.high,
        expected_constraints=["Macro basket daily move is usually below 3k."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_010",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_stat_arb_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[108.0, 109.0, 110.0, 720.0, 111.0],
        issue_type="anomaly",
        constraints=[
            "Stat-arb P&L variance remains below 3k in normal markets.",
            "No model or universe change occurred on Thu.",
        ],
        analyst_note="Repair the outlier and finalize.",
        history_summary="Observed days are smooth except for a single spike.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=110.5,
        expected_severity=Severity.high,
        expected_constraints=["Stat-arb P&L variance remains below 3k in normal markets."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_011",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_delta1_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[84.0, 85.0, 86.0, 530.0, 87.0],
        issue_type="anomaly",
        constraints=[
            "Delta-one daily change generally stays below 3k.",
            "No rebalance exception happened on Thu.",
        ],
        analyst_note="Take a high-confidence anomaly repair action.",
        history_summary="Series trend is stable and low-noise.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=86.5,
        expected_severity=Severity.high,
        expected_constraints=["Delta-one daily change generally stays below 3k."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_002",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_city_demand_forecast_mw",
        timestamps=["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
        values=[880.0, 920.0, 960.0, 1145.0, 1040.0, 1005.0],
        issue_type="invalid_forecast",
        constraints=[
            "Pre-peak demand should rise by roughly 30-50 MW/hour.",
            "At 20:00, demand must remain below 1100 MW due to transfer limits.",
            "After the peak window, demand should decline smoothly.",
        ],
        analyst_note="Check compliance with operations limits and escalate if needed.",
        history_summary="Evening load follows a constrained peak profile.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=1000.0,
        expected_severity=Severity.high,
        expected_constraints=["At 20:00, demand must remain below 1100 MW due to transfer limits."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_003",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_subregion_load_forecast_mw",
        timestamps=["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
        values=[760.0, 800.0, 840.0, 1120.0, 910.0, 880.0],
        issue_type="invalid_forecast",
        constraints=[
            "Demand should increase by around 30-50 MW/hour before peak.",
            "At 21:00, forecast must stay below 1000 MW due to N-1 security margin.",
            "Post-peak demand should trend downward.",
        ],
        analyst_note="Validate against the N-1 limit and escalation policy.",
        history_summary="Forecast should respect strict security cap at the peak.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=960.0,
        expected_severity=Severity.high,
        expected_constraints=["At 21:00, forecast must stay below 1000 MW due to N-1 security margin."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_004",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_balancing_area_forecast_mw",
        timestamps=["16:00", "17:00", "18:00", "19:00", "20:00", "21:00"],
        values=[690.0, 730.0, 770.0, 1055.0, 860.0, 830.0],
        issue_type="invalid_forecast",
        constraints=[
            "Ramp before peak should stay near +30 to +50 MW/hour.",
            "At 19:00, forecast must remain below 920 MW due to line derating.",
            "After peak, demand should decrease.",
        ],
        analyst_note="This forecast may violate line derating limits.",
        history_summary="System is operating under temporary transmission constraints.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=810.0,
        expected_severity=Severity.high,
        expected_constraints=["At 19:00, forecast must remain below 920 MW due to line derating."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_005",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_industrial_zone_forecast_mw",
        timestamps=["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
        values=[540.0, 575.0, 610.0, 910.0, 670.0, 640.0],
        issue_type="invalid_forecast",
        constraints=[
            "Normal evening ramp is +25 to +40 MW/hour.",
            "At 20:00, forecast must remain below 760 MW due to feeder maintenance.",
            "Demand should soften after the peak hour.",
        ],
        analyst_note="Ensure forecast complies with feeder maintenance cap.",
        history_summary="Industrial load profile is predictable under this operating mode.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=645.0,
        expected_severity=Severity.high,
        expected_constraints=["At 20:00, forecast must remain below 760 MW due to feeder maintenance."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_006",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_urban_grid_forecast_mw",
        timestamps=["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
        values=[820.0, 860.0, 900.0, 1190.0, 980.0, 950.0],
        issue_type="invalid_forecast",
        constraints=[
            "Pre-peak slope should remain in the 30-50 MW/hour band.",
            "At 21:00, demand must stay below 1030 MW under contingency policy.",
            "Post-peak profile should decline.",
        ],
        analyst_note="Review for contingency-policy breach.",
        history_summary="Peak-hour controls are active in this area.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=940.0,
        expected_severity=Severity.high,
        expected_constraints=["At 21:00, demand must stay below 1030 MW under contingency policy."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_007",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_regional_peak_forecast_mw",
        timestamps=["15:00", "16:00", "17:00", "18:00", "19:00", "20:00"],
        values=[610.0, 650.0, 690.0, 980.0, 760.0, 735.0],
        issue_type="invalid_forecast",
        constraints=[
            "Lead-up to peak should rise by about 30-50 MW/hour.",
            "At 18:00, forecast must remain below 800 MW due to reserve margin rule.",
            "After peak period, values should move down.",
        ],
        analyst_note="Confirm reserve-margin compliance at the peak interval.",
        history_summary="Regional dispatch is tightly limited during this window.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=730.0,
        expected_severity=Severity.high,
        expected_constraints=["At 18:00, forecast must remain below 800 MW due to reserve margin rule."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_008",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_coastal_grid_forecast_mw",
        timestamps=["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
        values=[700.0, 738.0, 776.0, 1088.0, 850.0, 820.0],
        issue_type="invalid_forecast",
        constraints=[
            "Expected pre-peak ramp is roughly +30 to +45 MW/hour.",
            "At 20:00, demand must remain below 900 MW due to transformer loading cap.",
            "Profile should decline after the peak hour.",
        ],
        analyst_note="Assess transformer loading risk and escalation need.",
        history_summary="Coastal network is near thermal limits during evening peak.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=814.0,
        expected_severity=Severity.high,
        expected_constraints=["At 20:00, demand must remain below 900 MW due to transformer loading cap."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_009",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_north_zone_forecast_mw",
        timestamps=["16:00", "17:00", "18:00", "19:00", "20:00", "21:00"],
        values=[670.0, 705.0, 740.0, 1025.0, 810.0, 780.0],
        issue_type="invalid_forecast",
        constraints=[
            "Before peak, increments should be around 30-45 MW/hour.",
            "At 19:00, demand must remain below 860 MW because of corridor limits.",
            "Demand should not rebound upward after peak.",
        ],
        analyst_note="Check whether corridor-limit violation requires escalation.",
        history_summary="North zone has tight corridor constraints in peak hours.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=775.0,
        expected_severity=Severity.high,
        expected_constraints=["At 19:00, demand must remain below 860 MW because of corridor limits."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_010",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_south_zone_forecast_mw",
        timestamps=["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
        values=[730.0, 770.0, 810.0, 1095.0, 890.0, 860.0],
        issue_type="invalid_forecast",
        constraints=[
            "Ramp into peak should be 30-50 MW/hour.",
            "At 21:00, demand must stay below 930 MW due to substation maintenance.",
            "After the peak slot, demand should decline.",
        ],
        analyst_note="Validate against substation maintenance constraint.",
        history_summary="South zone is operating under temporary maintenance restrictions.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=850.0,
        expected_severity=Severity.high,
        expected_constraints=["At 21:00, demand must stay below 930 MW due to substation maintenance."],
        value_tolerance=10.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_011",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_east_west_intertie_forecast_mw",
        timestamps=["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
        values=[790.0, 830.0, 870.0, 1160.0, 950.0, 920.0],
        issue_type="invalid_forecast",
        constraints=[
            "Expected ramp before peak is around 30-50 MW/hour.",
            "At 20:00, forecast must remain below 980 MW because intertie transfer is capped.",
            "Load should taper after the peak period.",
        ],
        analyst_note="Verify intertie cap compliance and escalate if violated.",
        history_summary="Intertie cap is the dominant operational constraint in this horizon.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=910.0,
        expected_severity=Severity.high,
        expected_constraints=["At 20:00, forecast must remain below 980 MW because intertie transfer is capped."],
        value_tolerance=10.0,
    ),
]

TASKS_BY_ID = {task.task_id: task for task in TASKS}
TASK_ORDER = [task.task_id for task in TASKS]


class ForecastAuditEnvironment:
    """Deterministic OpenEnv-style environment for mathematical forecast auditing."""

    def __init__(self) -> None:
        self._task_index = -1
        self._task: Optional[TaskSpec] = None
        self._observation: Optional[ForecastAuditObservation] = None
        self._done = False
        self._step_count = 0
        self._cumulative_score = 0.0
        self._reward_history: List[RewardModel] = []

    def reset(self, task_id: Optional[str] = None, difficulty: Optional[str] = None) -> ForecastAuditObservation:
        if task_id is not None:
            if task_id not in TASKS_BY_ID:
                raise ValueError(f"Unknown task_id: {task_id}")
            task = TASKS_BY_ID[task_id]
        elif difficulty is not None:
            matches = [task for task in TASKS if task.difficulty == difficulty]
            if not matches:
                raise ValueError(f"Unknown difficulty: {difficulty}")
            task = matches[0]
        else:
            self._task_index = (self._task_index + 1) % len(TASKS)
            task = TASKS[self._task_index]

        self._task = task
        self._done = False
        self._step_count = 0
        self._cumulative_score = 0.0
        self._reward_history = []
        self._observation = self._build_observation(task)
        return self._observation

    def state(self) -> ForecastAuditState:
        if self._task is None or self._observation is None:
            raise RuntimeError("Environment has not been reset yet.")
        return ForecastAuditState(
            task_id=self._task.task_id,
            difficulty=self._task.difficulty,
            current_observation=self._observation,
            done=self._done,
            step_count=self._step_count,
            max_steps=self._task.max_steps,
            cumulative_score=round(self._cumulative_score, 4),
            expected_action={
                "operation": self._task.expected_operation.value,
                "target_index": self._task.expected_index,
                "predicted_value": self._task.expected_value,
                "severity": self._task.expected_severity.value if self._task.expected_severity else None,
                "violated_constraints": self._task.expected_constraints,
            },
            reward_history=self._reward_history,
        )

    def step(
        self, action: ForecastAuditAction
    ) -> Tuple[ForecastAuditObservation, RewardModel, bool, Dict[str, Any]]:
        if self._task is None or self._observation is None:
            raise RuntimeError("Call reset() before step().")
        if self._done:
            raise RuntimeError("Episode already completed. Call reset() to start a new one.")

        self._step_count += 1
        reward = self._grade_action(self._task, action, self._step_count)
        self._reward_history.append(reward)
        self._cumulative_score += reward.score

        if reward.score >= 0.95:
            self._done = True
        elif self._step_count >= self._task.max_steps:
            self._done = True

        self._observation = self._advance_observation(action, reward)
        info = {
            "task_id": self._task.task_id,
            "difficulty": self._task.difficulty,
            "issue_type": self._task.issue_type,
            "max_steps": self._task.max_steps,
            "step_count": self._step_count,
            "expected_operation": self._task.expected_operation.value,
        }
        return self._observation, reward, self._done, info

    def _build_observation(self, task: TaskSpec) -> ForecastAuditObservation:
        return ForecastAuditObservation(
            task_id=task.task_id,
            difficulty=task.difficulty,
            domain=task.domain,
            metric_name=task.metric_name,
            timestamps=copy.deepcopy(task.timestamps),
            values=copy.deepcopy(task.values),
            issue_type=task.issue_type,
            constraints=copy.deepcopy(task.constraints),
            analyst_note=task.analyst_note,
            step_count=0,
            max_steps=task.max_steps,
            history_summary=task.history_summary,
        )

    def _advance_observation(
        self, action: ForecastAuditAction, reward: RewardModel
    ) -> ForecastAuditObservation:
        assert self._task is not None
        values = copy.deepcopy(self._observation.values if self._observation else self._task.values)
        if action.target_index is not None and action.predicted_value is not None:
            if 0 <= action.target_index < len(values):
                values[action.target_index] = float(action.predicted_value)

        analyst_note = (
            f"Previous action: {action.operation.value}. "
            f"Reward={reward.score:.2f}. {reward.message}"
        )
        return ForecastAuditObservation(
            task_id=self._task.task_id,
            difficulty=self._task.difficulty,
            domain=self._task.domain,
            metric_name=self._task.metric_name,
            timestamps=copy.deepcopy(self._task.timestamps),
            values=values,
            issue_type=self._task.issue_type,
            constraints=copy.deepcopy(self._task.constraints),
            analyst_note=analyst_note,
            step_count=self._step_count,
            max_steps=self._task.max_steps,
            history_summary=self._task.history_summary,
        )

    def _grade_action(self, task: TaskSpec, action: ForecastAuditAction, step_count: int) -> RewardModel:
        components: Dict[str, float] = {
            "operation": 0.0,
            "index": 0.0,
            "value": 0.0,
            "severity": 0.0,
            "constraints": 0.0,
            "rationale": 0.0,
            "efficiency": 0.0,
            "penalty": 0.0,
        }

        if action.operation == task.expected_operation:
            components["operation"] = 0.35
        elif task.issue_type == "anomaly" and action.operation == Operation.flag_anomaly:
            components["operation"] = 0.2
        elif task.issue_type == "invalid_forecast" and action.operation == Operation.repair_and_finalize:
            components["operation"] = 0.15

        if action.target_index == task.expected_index:
            components["index"] = 0.15

        if task.expected_value is not None and action.predicted_value is not None:
            error = abs(action.predicted_value - task.expected_value)
            if error <= task.value_tolerance:
                components["value"] = 0.2
            elif error <= task.value_tolerance * 2:
                components["value"] = 0.1

        if task.expected_severity is not None and action.severity == task.expected_severity:
            components["severity"] = 0.1

        if task.expected_constraints:
            matched_constraints = set(action.violated_constraints).intersection(task.expected_constraints)
            if matched_constraints:
                components["constraints"] = min(0.1, 0.1 * len(matched_constraints) / len(task.expected_constraints))
        else:
            if not action.violated_constraints:
                components["constraints"] = 0.1

        rationale_lower = action.rationale.lower()
        if len(action.rationale.split()) >= 5:
            components["rationale"] = 0.05
        if any(keyword in rationale_lower for keyword in ["missing", "anomaly", "capacity", "linear", "trend", "repair", "escalate"]):
            components["rationale"] = max(components["rationale"], 0.08)

        components["efficiency"] = max(0.0, 0.05 - (step_count - 1) * 0.02)

        penalty = 0.0
        if action.operation == Operation.accept and task.issue_type != "missing_value":
            penalty += 0.15
        if action.operation == Operation.accept and task.issue_type == "missing_value":
            penalty += 0.25
        if action.operation == Operation.impute and action.predicted_value is None:
            penalty += 0.2
        if action.operation in (Operation.repair_and_finalize, Operation.impute) and action.target_index is None:
            penalty += 0.15
        if not action.rationale:
            penalty += 0.05
        components["penalty"] = -penalty

        raw_score = sum(value for key, value in components.items() if key != "penalty") - penalty
        final_score = max(0.01, min(0.99, round(raw_score, 4)))

        message = self._build_feedback_message(task, action, final_score)
        return RewardModel(score=final_score, components=components, message=message)

    @staticmethod
    def _build_feedback_message(task: TaskSpec, action: ForecastAuditAction, final_score: float) -> str:
        if final_score >= 0.95:
            return "Excellent action. The issue was handled correctly and can be finalized."
        if action.operation == Operation.accept:
            return "Accepting this record leaves a known issue unresolved."
        if task.issue_type == "missing_value" and action.operation != Operation.impute:
            return "This task primarily requires imputing the missing point."
        if task.issue_type == "anomaly" and action.operation not in (Operation.flag_anomaly, Operation.repair_and_finalize):
            return "The core challenge is spotting and handling the anomalous point."
        if task.issue_type == "invalid_forecast" and action.operation != Operation.escalate:
            return "This forecast violates an operational constraint and should likely be escalated."
        return "Partial progress. Tighten the operation choice, index, value, or constraints cited."
