# apiTester
Testing framework to simplify creating unit tests for your API's. Supports mocks and mock assertions.

The goal with this project is to provide a simple way to define unit tests for your API using yaml configuration files. This should still be compatible with python based unittest runners. 

Tests are defined in yaml files in order to be human readable and easy to understand. Tests supports starting up mock services to allow you to test API services that perform orchestration. Assertions can be defined on a global service level (request-response pattern) and also on mock steps to verify that the correct message was sent to the mock service.

API Tester supports executing python code in setup and teardown methods.
