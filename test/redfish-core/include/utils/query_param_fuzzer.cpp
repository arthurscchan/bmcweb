// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright OpenBMC Authors

#include "filter_expr_executor.hpp"
#include "filter_expr_printer.hpp"
#include "http_response.hpp"
#include "utils/query_param.hpp"

#include <boost/url/params_view.hpp>
#include <boost/url/parse.hpp>
#include <boost/url/url_view.hpp>
#include <nlohmann/json.hpp>

#include <cstddef>
#include <cstdint>
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

    // 1. The whole query string, as it arrives on a Redfish URL.
    std::string target = "/redfish/v1/Systems?";
    target += input;
    boost::system::result<boost::urls::url_view> url =
        boost::urls::parse_relative_ref(target);
    if (url)
    {
        crow::Response res;
        std::optional<redfish::query_param::Query> query =
            redfish::query_param::parseParameters(url->params(), res);
        (void)query;
    }

    // 2. The same bytes as a bare $filter expression, so the grammar is
    //    driven directly rather than only through a well-formed URL.
    std::optional<redfish::filter_ast::LogicalAnd> program =
        redfish::parseFilter(input);
    if (program)
    {
        nlohmann::json body = nlohmann::json::parse(
            R"({"Members":[{"Id":"1","Name":"a","Count":3},
                           {"Id":"2","Name":"b","Count":0}],
                "Members@odata.count":2})",
            nullptr, false);
        if (!body.is_discarded())
        {
            redfish::applyFilterToCollection(body, *program);
        }
    }

    return 0;
}
