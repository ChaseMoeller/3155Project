Feature: Edit an question/post

User Story: As a user I want to be able to edit a question/post so I can fix or change my initial post.

Scenario:
	Given I am on the “recent posts” page
	When I click on the “edit” link
	Then I am on the “edit post” page
	When I edit the text in the title and body boxes and click the “edit post” button
  Then the post is updated with new text and I am back on the “recent posts” page for the updated post
