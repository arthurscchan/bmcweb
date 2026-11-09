// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright OpenBMC Authors

// Fuzzer for the Redfish query-parameter parser
// (redfish-core/include/utils/query_param.hpp).
//
// Every Redfish request's query string flows through parseParameters() before
// any handler runs, so the parser sees fully attacker-controlled key/value
// pairs.  The harness treats the whole fuzz input as a query parameter string
// (the part of a URI after '?'), exercises parseParameters() including the
// error paths that write Redfish error messages into the response, and then
// drives the delegation and expand-formatting logic over the parsed result.
//
// Expected bug classes: memory safety in the select-trie and expand-level
// handling, integer overflows in numeric parameters, logic errors in the
// filter expression parser, and pathological blowups in recursive select
// application.

#include "http_response.hpp"
#include "utils/query_param.hpp"

#include <boost/url/params_view.hpp>

#include <cstdint>
#include <cstddef>
#include <optional>
#include <string>
#include <string_view>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    if (size == 0 || size > 4096)
    {
        return 0;
    }
    std::string_view input(reinterpret_cast<const char*>(data), size);

    boost::urls::params_view urlParams(input);
    crow::Response res;
    std::optional<redfish::query_param::Query> query =
        redfish::query_param::parseParameters(urlParams, res);
    if (!query)
    {
        // Invalid parameter combinations were already exercised through the
        // error-message paths above.
        return 0;
    }

    redfish::query_param::QueryCapabilities capabilities;
    capabilities.canDelegateOnly = true;
    capabilities.canDelegateTop = true;
    capabilities.canDelegateSkip = true;
    capabilities.canDelegateSelect = true;
    capabilities.canDelegateExpandLevel = 3;
    redfish::query_param::Query delegated =
        redfish::query_param::delegate(capabilities, *query);
    (void)delegated;

    std::optional<std::string> formatted =
        redfish::query_param::formatQueryForExpand(*query);
    (void)formatted;

    return 0;
}
