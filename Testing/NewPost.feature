Feature: Create a question/post

User Story: As a user I want to be able to create a question/post so I can communicate with others.

Scenario:
	Given I am on the home page
	When I click on the “new posts” link
	Then I am on the “new post” page
	When I enter text in the title and body boxes and click the “create post” button
	Then the post is added to “recent posts” and I am on that page
