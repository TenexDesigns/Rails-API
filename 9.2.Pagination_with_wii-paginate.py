API pagination is a technique used to split large result sets into smaller chunks or pages to improve 
performance and provide a better user experience. In a Rails API app, you can implement pagination using various approaches.
One common approach is to use the will_paginate gem along with the page and per_page parameters.



To implement API pagination in a Rails API app, you can use popular pagination libraries like
will_paginate or kaminari along with the api-pagination gem, which automatically sets the Link header 
for paginated responses thecodeboss.dev.




Heres an example of implementing pagination using will_paginate and api-pagination:

1.Add the following gems to your Gemfile:
# Gemfile
gem 'will_paginate'

2.Run bundle install to install the gems.

3.Modify the controller action: In the controller action where you want to implement pagination,
  retrieve the paginated records using will_paginate and send them as a response.


def index
  records = Record.paginate(page: params[:page], per_page:10)
  render json: records
end

In this example, the paginate method is used to retrieve the paginated records based on the provided page and per_page parameters.



4.Set up the route: You can keep using the original router you were using, paginationation does not affect the router
  Update your routes file (config/routes.rb) to include the route for the paginated records.

resources :records, only: [:index]
This will create the necessary route for the index action of the RecordsController.





5.Send pagination parameters: In the API request, include the page and per_page parameters to control the pagination.

For example, you can make a GET request to /records?page=1 or to retrieve the first page with 10 records per page.





By following these steps, you can implement API pagination in your Rails API app using the will_paginate gem. 
You can customize the pagination logic further by modifying the paginate method options or by using
additional gem options like total_entries or total_pages to provide pagination metadata in the response.






Eager loading in pagination to avoid N+1 queries.
_______________________________________________________________________________________________________________________________

To avoid the N+1 query problem, you can use eager loading. 
Eager loading allows you to fetch the associated records in a single query,
reducing the number of database trips.
In Rails, you can use the includes method to eager load associations.

Heres how you can modify the code to use eager loading:

Retrieve the paginated posts with eager loading:

posts = Post.includes(:user).paginate(page: params[:page], 
                                      
The includes(:user) tells Rails to fetch the associated user records in the same query that fetches the posts.
  # This line does not trigger additional queries 
By eager loading the user association using includes(:user),
 Rails fetches the associated users in a single query upfront,
 avoiding the need for separate queries for each post.
 This significantly improves performance and eliminates the N+1 query problem.

Eager loading is an essential technique to optimize database queries and reduce the number of database
round-trips when dealing with associations,
 especially in scenarios like pagination where you are retrieving a subset of records along with their associated data.
                                      
Practical example

        def index

          books = Book2.includes(:author).paginate(page: params[:page],per_page:3)
          render json: books

        end










customisation
***********************************************************************************************************************

Certainly! The will_paginate gem provides several customization options and additional features for API pagination in your Rails API app.
 Here are some of the key customization options and further information:

Customizing the number of records per page: By default, will_paginate uses 30 records per page.
 You can customize this value by setting the per_page option when calling the paginate method.

records = Record.paginate(page: params[:page], per_page: 10)
In this example, each page will contain 10 records.

Accessing pagination metadata: The will_paginate gem provides metadata about the pagination, 
  such as the total number of pages and the total number of records. 
  You can access this information using the total_pages and total_entries methods.


records = Record.paginate(page: params[:page], per_page: 10)
total_pages = records.total_pages
total_entries = records.total_entries
You can include this metadata in the API response to provide additional information to clients.

Handling edge cases: will_paginate automatically handles edge cases such as requesting a page that exceeds the total number of pages. 
 If an invalid page number is specified, it will return an empty collection.

Customizing the pagination view: will_paginate provides a default pagination view, but you can customize it 
 to match your applications styling. You can generate the default view 
  template by running the following command in your terminal:

Copy code
rails generate will_paginate:views
This command generates a view file (_paginator.html.erb) that you can modify as needed.

Additional customization options: The paginate method accepts additional options to customize the pagination behavior.
Some commonly used options include:

order: Specifies the ordering of the records.
conditions: Adds additional conditions to filter the records.
include: Eager loads associations to avoid N+1 queries.
You can refer to the will_paginate documentation for more details on these options and other customization possibilities.

By leveraging these customization options, you can fine-tune the pagination functionality in your Rails API app to
 suit your specific requirements.






















.....
