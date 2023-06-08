To implement JWT authentication in your Rails API app, follow these steps:

1.Add the required gems to your Gemfile and run bundle install:
# Gemfile
gem 'jwt'
gem 'bcrypt'

2.Create a user model and controller:
rails generate model User email:string password_digest:string
rails generate controller Api::V1::Users
        
3.Add has_secure_password to the User model:
# app/models/user.rb
class User < ApplicationRecord
  has_secure_password
  validates :email, presence: true, uniqueness: true
end

4.Create an AuthenticationController to handle user login:
rails generate controller Api::V1::Authentication
        
5.Add a method to encode and decode JWT tokens in ApplicationController:
# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  def encode_token(payload)
    JWT.encode(payload, ENV['JWT_SECRET'])
  end

  def decode_token(token)
    JWT.decode(token, ENV['JWT_SECRET'])[0]
  end
end

6.Implement the login action in AuthenticationController:
# app/controllers/api/v1/authentication_controller.rb
class Api::V1::AuthenticationController < ApplicationController
  def create
    user = User.find_by(email: params[:email])
    if user && user.authenticate(params[:password])
      token = encode_token({ user_id: user.id })
      render json: { token: token }
    else
      render json: { error: 'Invalid email or password' }, status: :unauthorized
    end
  end
end

7.Add routes for user creation and login:
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :users, only: [:create]
      post '/login', to: 'authentication#create'
    end
  end
end

8.Create a method to enforce authentication on endpoints:
# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  before_action :authorized
  
  def encode_token(payload)
      JWT.encode(payload, ENV['JWT_SECRET'])
  end
    
  def decode_token(token)
      JWT.decode(token, ENV['JWT_SECRET'])[0]
  end  

  def authorized
    render json: { error: 'Please log in' }, status: :unauthorized unless logged_in?
  end

  def logged_in?
    current_user.present?
  end

  def current_user
    if decoded_token
      user_id = decoded_token['user_id']
      @user ||= User.find_by(id: user_id)
    end
  end

  def decoded_token
    token = request.headers['Authorization']
    begin
      decode_token(token)
    rescue JWT::DecodeError
      nil
    end
  end
end

9.Add skip_before_action to the UsersController to allow user registration without authentication:
# app/controllers/api/v1/users_controller.rb
class Api::V1::UsersController < ApplicationController
  skip_before_action :authorized, only: [:create]

  def create
    user = User.new(user_params)
    if user.save
      token = encode_token({ user_id: user.id })
      render json: { user: user, token: token }
    else
      render json: { error: user.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  def user_params
    params.require(:user).permit(:email, :password)
  end
end
Now you can enforce authentication on any endpoint by inheriting from ApplicationController.
Users can register and log in using the /api/v1/users and /api/v1/login endpoints, respectively.
The client should include the JWT token in the Authorization header for any request that requires authentication.





TO CREATE A SUSE
*************************************************************************8

1.Create a user:
  
a.->Set the HTTP method to POST
b.->Enter the URL: http://localhost:3000/api/v1/users (Replace localhost:3000 with your API's address if it's hosted elsewhere)
c.->Go to the Body tab
d.->Select raw and choose JSON from the dropdown menu
e.->Enter the user data in JSON format:

{
  "user": {
    "email": "example@example.com",
    "password": "George1"
  }
}









has_secure_password 
*****************************************************************************************
The has_secure_password method, provided by the bcrypt Ruby gem, is responsible for hashing and 
salting the password before storing it in the password_digest column dev.to. 
This method also generates an authenticate method, which can be used to verify the users password during the login process.









in the above context, what is this present in the line current_user.present?
*****************************************************************************************

The present? method in the line current_user.present? is called on the current_user object to check if the user exists.
In Rails, present? is the opposite of blank?. It returns true if the object is not nil and not
empty (in case it's a string, array, or hash) stackoverflow.com.

In the context of the logged_in? method, current_user.present? checks if there is a valid current_user object,
       meaning that a user is logged in. If current_user is nil or empty, present? will return false, 
       indicating that the user is not logged in.







In the above context,what does this code do
*******************************************************************************
       # app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  before_action :authorized

  def authorized
    render json: { error: 'Please log in' }, status: :unauthorized unless logged_in?
  end

  def logged_in?
    current_user.present?
  end

  def current_user
    if decoded_token
      user_id = decoded_token['user_id']
      @user ||= User.find_by(id: user_id)
    end
  end

  def decoded_token
    token = request.headers['Authorization']
    begin
      decode_token(token)
    rescue JWT::DecodeError
      nil
    end
  end
end
       
In the provided code, the ApplicationController is responsible for handling authentication and user authorization. It contains several methods to manage JWT and user authentication. Here's a breakdown of each method:

before_action :authorized: This line ensures that the authorized method is called before any action in the controllers 
       that inherit from ApplicationController. This helps enforce authentication on the endpoints.
       
authorized: This method checks if the user is logged in by calling the logged_in? method. If the user is not logged in,
       it renders a JSON error message with a status of :unauthorized.
       
logged_in?: This method checks if a current_user is present. If current_user is not nil, it means the user is logged in.
       
current_user: This method retrieves the current user from the decoded JWT token. If the decoded_token is present,
       it obtains the user_id from the token and finds the corresponding user in the database.
       The user is then memoized using the @user instance variable to avoid multiple database queries.
       
decoded_token: This method extracts the JWT token from the Authorization header and attempts to decode it.
       If the token is valid, it returns the decoded token payload; otherwise, it returns nil.
       
In summary, the provided code enforces authentication on the endpoints of the Rails API app.
       It does so by checking if the user is logged in before executing any action in the controllers 
       that inherit from ApplicationController. 
       The users authentication status is determined by the presence of a valid JWT token in the Authorization header of the request.






1.ERRORS I ENCOUNTERED
***************************************************************************************************
To avoid confusion regarding the format of the request data, it is essential to establish a clear communication between the frontend and backend developers. The frontend developers should be aware of the expected format for the request payload, which can be documented in API documentation or shared through other communication channels.

In your specific case, the expected format of the request payload is determined by the memeber_params method in your MemebersController:

def memeber_params
  params.require(:memeber).permit(:email, :password)
end
This method indicates that the email and password parameters should be nested under the memeber key. Therefore, the frontend developers should send the request payload in the following format:

{
  "memeber": {
    "email": "example@example.com",
    "password": "George1"
  }
}
To avoid confusion in the future, consider creating API documentation that clearly outlines the expected request payload format for each endpoint. This will help frontend developers understand how to structure their requests and reduce the likelihood of errors related to incorrect request payloads. You can use tools like Swagger or Postman to create and maintain API documentation.






2.ERRORS I ENCOUNTERED
***************************************************************************************************


The NoMethodError (undefined method 'password_digest=') error occurs when the has_secure_password method is used in a model, but the corresponding password_digest column is missing in the database table. The has_secure_password method expects the password_digest column to store the hashed password.

To fix this issue, you need to add the password_digest column in your memebers table:

Generate a migration to add the password_digest column:
rails generate migration AddPasswordDigestToMemebers password_digest:string
This will create a migration file with the following content:
class AddPasswordDigestToMemebers < ActiveRecord::Migration[6.0]
  def change
    add_column :memebers, :password_digest, :string
  end
end
Run the migration to update the database:
rails db:migrate
Now, the password_digest column should be added to the memebers table, and the error should be resolved.

If you are using Devise for authentication, make sure your Memeber model inherits from ApplicationRecord and includes the necessary Devise modules, similar to the User model in the previous example:

class Memeber < ApplicationRecord
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable,
         :jwt_authenticatable, jwt_revocation_strategy: JwtDenylist
end
This configuration ensures that the Devise authentication system handles password hashing and storage correctly.























































































































































































..
