#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright OpenBMC Authors
"""Generate a seed corpus for the http_connection_fuzzer.

The connection fuzzer feeds its whole input as client bytes into an in-memory
socket, so each seed is one raw HTTP/1.1 request.  bmcweb's Redfish handlers
are only exercised when a request hits a registered route with a plausible
URI; without seeds the fuzzer never gets past random byte soup.  The seeds
here cover the top-level service, collection and instance URIs of the major
Redfish resources, plus query-parameter variants ($expand/$select/$top/$skip/
only/$filter) that drive the query and filter parsers, and a few invalid
values that exercise the error-message paths.

Usage: generate_seeds.py <output-zip>
"""

import zipfile

HEADERS = "Host: 127.0.0.1\r\nAccept: application/json\r\n"


def get(uri: str, version: str = "HTTP/1.1") -> bytes:
    return (f"GET {uri} {version}\r\n{HEADERS}\r\n").encode()


def seeds() -> dict[str, bytes]:
    data: dict[str, bytes] = {}

    def add(name: str, uri: str) -> None:
        data[name] = get(uri.replace("\\$", "$"))

    # Service root and metadata
    add("service_root", "/redfish/v1/")
    data["redfish_index"] = get("/redfish/")
    data["service_root_noslash"] = get("/redfish/v1")
    add("metadata", "/redfish/v1/$metadata/")

    # Systems family
    add("systems_collection", "/redfish/v1/Systems/")
    add("systems_instance", "/redfish/v1/Systems/system/")
    add("systems_processors", "/redfish/v1/Systems/system/Processors/")
    add("systems_processor", "/redfish/v1/Systems/system/Processors/cpu0/")
    add("systems_memory", "/redfish/v1/Systems/system/Memory/")
    add("systems_memory_dimm", "/redfish/v1/Systems/system/Memory/dimm0/")
    add("systems_storage", "/redfish/v1/Systems/system/Storage/")
    add("systems_storage_ctrl",
        "/redfish/v1/Systems/system/Storage/1/Controllers/")
    add("systems_pcie", "/redfish/v1/Systems/system/PCIeDevices/")
    add("systems_bios", "/redfish/v1/Systems/system/Bios/")
    add("systems_fabric", "/redfish/v1/Systems/system/FabricAdapters/")
    add("systems_logservices", "/redfish/v1/Systems/system/LogServices/")
    add("systems_eventlog_entries",
        "/redfish/v1/Systems/system/LogServices/EventLog/Entries/")
    add("systems_dump_entries",
        "/redfish/v1/Systems/system/LogServices/Dump/Entries/")
    add("systems_postcodes",
        "/redfish/v1/Systems/system/LogServices/PostCodes/")
    add("systems_hostlogger",
        "/redfish/v1/Systems/system/LogServices/HostLogger/")
    add("systems_crashdump",
        "/redfish/v1/Systems/system/LogServices/Crashdump/")

    # Chassis family
    add("chassis_collection", "/redfish/v1/Chassis/")
    add("chassis_instance", "/redfish/v1/Chassis/chassis/")
    add("chassis_sensors", "/redfish/v1/Chassis/chassis/Sensors/")
    add("chassis_sensor", "/redfish/v1/Chassis/chassis/Sensors/temp0/")
    add("chassis_power", "/redfish/v1/Chassis/chassis/Power/")
    add("chassis_thermal", "/redfish/v1/Chassis/chassis/Thermal/")
    add("chassis_power_supplies",
        "/redfish/v1/Chassis/chassis/PowerSubsystem/PowerSupplies/")
    add("chassis_fans", "/redfish/v1/Chassis/chassis/ThermalSubsystem/Fans/")
    add("chassis_pcie_slots", "/redfish/v1/Chassis/chassis/PCIeSlots/")
    add("chassis_net_adapters", "/redfish/v1/Chassis/chassis/NetworkAdapters/")
    add("chassis_drives", "/redfish/v1/Chassis/chassis/Drives/")
    add("chassis_env_metrics",
        "/redfish/v1/Chassis/chassis/EnvironmentMetrics/")
    add("chassis_assembly", "/redfish/v1/Chassis/chassis/Assembly/")

    # Managers family
    add("managers_collection", "/redfish/v1/Managers/")
    add("managers_instance", "/redfish/v1/Managers/bmc/")
    add("managers_ethernet", "/redfish/v1/Managers/bmc/EthernetInterfaces/")
    add("managers_ethernet_iface",
        "/redfish/v1/Managers/bmc/EthernetInterfaces/eth0/")
    add("managers_logservices", "/redfish/v1/Managers/bmc/LogServices/")
    add("managers_journal_entries",
        "/redfish/v1/Managers/bmc/LogServices/Journal/Entries/")
    add("managers_virtualmedia", "/redfish/v1/Managers/bmc/VirtualMedia/")
    add("managers_networkprotocol", "/redfish/v1/Managers/bmc/NetworkProtocol/")
    add("managers_oem", "/redfish/v1/Managers/bmc/Oem/")

    # Account and session service
    add("account_service", "/redfish/v1/AccountService/")
    add("account_accounts", "/redfish/v1/AccountService/Accounts/")
    add("account_account", "/redfish/v1/AccountService/Accounts/operator/")
    add("account_roles", "/redfish/v1/AccountService/Roles/")
    add("account_role", "/redfish/v1/AccountService/Roles/Administrator/")
    add("account_ldap_certs", "/redfish/v1/AccountService/LDAP/Certificates/")
    add("session_service", "/redfish/v1/SessionService/")
    add("session_sessions", "/redfish/v1/SessionService/Sessions/")

    # Other services
    add("certificate_service", "/redfish/v1/CertificateService/")
    add("cert_locations",
        "/redfish/v1/CertificateService/CertificateLocations/")
    add("update_service", "/redfish/v1/UpdateService/")
    add("firmware_inventory", "/redfish/v1/UpdateService/FirmwareInventory/")
    add("event_service", "/redfish/v1/EventService/")
    add("event_subscriptions", "/redfish/v1/EventService/Subscriptions/")
    add("task_service", "/redfish/v1/TaskService/")
    add("task_tasks", "/redfish/v1/TaskService/Tasks/")
    add("telemetry_service", "/redfish/v1/TelemetryService/")
    add("telemetry_mrd", "/redfish/v1/TelemetryService/MetricReportDefinitions/")
    add("telemetry_triggers", "/redfish/v1/TelemetryService/Triggers/")
    add("telemetry_reports", "/redfish/v1/TelemetryService/MetricReports/")
    add("aggregation_service", "/redfish/v1/AggregationService/")
    add("aggregation_sources",
        "/redfish/v1/AggregationService/AggregationSources/")
    add("cables", "/redfish/v1/Cables/")
    add("fabrics", "/redfish/v1/Fabrics/")
    add("json_schemas", "/redfish/v1/JsonSchemas/")
    add("registries", "/redfish/v1/Registries/")

    # Query parameter variants against rich resources
    add("query_expand_star", "/redfish/v1/Systems/system/?\\$expand=*")
    add("query_expand_dot", "/redfish/v1/Systems/system/?\\$expand=.")
    add("query_expand_levels",
        "/redfish/v1/Systems/system/?\\$expand=*($levels=2)")
    add("query_expand_named", "/redfish/v1/Chassis/chassis/?\\$expand=Chassis")
    add("query_expand_multi",
        "/redfish/v1/Chassis/chassis/?\\$expand=Power,Thermal")
    add("query_select",
        "/redfish/v1/Systems/system/?\\$select=Id,PowerState")
    add("query_select_nested",
        "/redfish/v1/Chassis/chassis/?\\$select=Status/Health")
    add("query_top_skip",
        "/redfish/v1/Systems/system/Processors/?\\$top=1&\\$skip=1")
    add("query_only", "/redfish/v1/Systems/system/?only")
    add("query_filter",
        "/redfish/v1/Systems/system/Processors/?\\$filter=Id=cpu0")
    add("query_filter_ne",
        "/redfish/v1/Systems/system/Processors/?\\$filter=Health=^OK")
    add("query_combined",
        "/redfish/v1/Chassis/chassis/?\\$expand=*($levels=1)&\\$select=Id&\\$top=2")

    # Invalid values exercising error-message paths
    add("query_only_bad", "/redfish/v1/Systems/system/?only=unexpected")
    add("query_expand_bad", "/redfish/v1/Systems/system/?\\$expand=bogus")
    add("query_top_overflow",
        "/redfish/v1/Systems/system/Processors/?\\$top=99999999999999999999")
    add("query_skip_negative",
        "/redfish/v1/Systems/system/Processors/?\\$skip=-1")
    add("query_unknown", "/redfish/v1/Systems/system/?unknownparam=1")

    # Not-found resource (error path with route hit)
    add("missing_resource", "/redfish/v1/Systems/nosuchsystem/")

    # Protocol variants
    data["http10_request"] = get("/redfish/v1/", version="HTTP/1.0")
    data["head_request"] = (
        "HEAD /redfish/v1/ HTTP/1.1\r\n" + HEADERS + "\r\n").encode()
    return data


def main() -> None:
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output-zip>", file=sys.stderr)
        raise SystemExit(1)
    out = sys.argv[1]
    corpus = seeds()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for index, (name, payload) in enumerate(sorted(corpus.items()), 1):
            z.writestr(f"{index:04d}_{name}", payload)
    print(f"wrote {len(corpus)} seeds to {out}")


if __name__ == "__main__":
    main()

