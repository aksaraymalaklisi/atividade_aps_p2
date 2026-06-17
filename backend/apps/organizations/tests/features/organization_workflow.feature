Feature: Organization Approval Workflow
  As a User
  I want to register an organization
  So that I can use the platform as an NGO or independent protector

  Scenario: User registers an organization successfully
    Given a logged in user with email "user@test.com"
    When the user submits a registration for an organization named "Animais Felizes"
    Then the organization should be created with status "PENDING"
    And the user should be the "OWNER" of the organization

  Scenario: Operator approves an organization
    Given a logged in operator with email "admin@test.com"
    And an existing pending organization named "Pending ONG"
    When the operator approves the organization "Pending ONG"
    Then the organization status should be "APPROVED"

  Scenario: Operator rejects an organization
    Given a logged in operator with email "admin2@test.com"
    And an existing pending organization named "Bad ONG"
    When the operator rejects the organization "Bad ONG" with reason "Fake documents"
    Then the organization status should be "REJECTED"
