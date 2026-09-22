#include <iostream>
#include <nlohmann/json-schema.hpp>

using nlohmann::json;
using nlohmann::json_schema::json_validator;

static const json rectangle_schema = R"(
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "A rectangle",
    "properties": {
        "width": {
            "$ref": "#/definitions/length",
            "default": 20
        },
        "height": {
            "$ref": "#/definitions/length"
        }
    },
    "definitions": {
        "length": {
            "type": "integer",
            "minimum": 1,
            "default": 10
        }
    }
})"_json;

int main()
{
    try {
        json_validator validator{rectangle_schema};
        /* validate empty json -> will be expanded by the default values defined in the schema */
        json rectangle = "{}"_json;
        const auto default_patch = validator.validate(rectangle);
        rectangle = rectangle.patch(default_patch);
        std::cout << rectangle.dump() << std::endl; // {"height":10,"width":20}
    } catch (const std::exception &e) {
        std::cerr << "Validation of schema failed: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}