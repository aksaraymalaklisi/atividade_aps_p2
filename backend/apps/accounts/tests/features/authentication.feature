Feature: User Registration and Authentication
  As a new visitor to the PetAdopt platform
  I want to register an account and log in
  So that I can use the platform's features

  Scenario: Successful User Registration
    Given I have a valid email "bdd_test@example.com" and username "bdd_user"
    And a secure password "SecurePass123!"
    When I submit the registration form
    Then I should receive a successful response with status 201
    And my new user account should be created in the system

  Scenario: Registration with Duplicate Email
    Given a user already exists with email "existing_bdd@example.com" and username "existing_user"
    When I submit the registration form with email "existing_bdd@example.com" and username "another_user"
    Then I should receive an error response with status 400
    And the error code should be "USER_ALREADY_EXISTS"

  Scenario: Successful Login
    Given a user already exists with email "login_bdd@example.com" and password "LoginPass123!"
    When I submit the login form with email "login_bdd@example.com" and password "LoginPass123!"
    Then I should receive a successful response with status 200
    And the response should contain access and refresh JWT tokens
