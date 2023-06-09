To implement JWT authentication in your Rails API app, follow these steps:

1.Add the required gems to your Gemfile and run bundle install:
# Gemfile
gem 'jwt'
gem 'bcrypt'

2.Create a user model and controller:
rails generate model Memeber email:string password_digest:string
rails generate controller Api::V1::Memeber
        
3.Add has_secure_password to the User model:
# app/models/user.rb
class Memeber < ApplicationRecord
  has_secure_password
  validates :email, presence: true, uniqueness: true
end

4.Create an AuthenticationController to handle user login:
rails generate controller Api::V1::Authentication
        
        
        
5.Add a service called AuthenticationTokenService to the services foleder in app encode and decode JWT tokens :
# app/services/authentication_token_servic.rb
class AuthenticationTokenService
    HMAC_SECRET = 'my$ecretK3y'
    ALGORITHM_TYPE ='HS256'

    def self.encode(user_id)
        payload = { user_id: user_id, exp:  exp: 1.minute.from_now.to_i  }
        JWT.encode payload , HMAC_SECRET,ALGORITHM_TYPE
    end

    def self.decode(token)
        decoded_token =JWT.decode token, HMAC_SECRET,true, {algorithm:ALGORITHM_TYPE}
        decoded_token[0]['user_id']
    end    

end
  
  
  
6.Implement the login action in AuthenticationController:
# app/controllers/api/v1/authentication_controller.rb
module Api
  module V1
  
      class AuthenticationController < ApplicationController
        require('D:\ruby\ruby1\nile\nile\app\services\authentication_token_service.rb')
          skip_before_action :authenticate_user, only: [:create]

          def create
              memeber = Memeber.find_by(email: params[:email])
              if memeber && memeber.authenticate(params[:password])
                token = AuthenticationTokenService.encode(memeber.id)
                render json: { token: token ,memeber: memeber}
              else
                render json: { error: 'Invalid email or password' }, status: :unauthorized
              end
          end
      end
  end
end    


7.Create a method to enforce authentication on all endpoints:
# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  require('D:\ruby\ruby1\nile\nile\app\services\authentication_token_service.rb')
  include ActionController::HttpAuthentication::Token

  before_action :authenticate_user

  def authenticate_user
    begin
      token, _options = token_and_options(request)
      memeber_id =AuthenticationTokenService.decode(token)
      Memeber.find(memeber_id)

    rescue ActiveRecord::RecordNotFound
      render json: { error: 'Invalid token' }, status: :unauthorized
    end
  end   
end


8.Add skip_before_action to the MemebersController to allow user registration without authentication:
# app/controllers/api/v1/users_controller.rb

module Api
  module V1

     class MemebersController < ApplicationController
          skip_before_action :authenticate_user, only: [:create]
          def create
              memeber = Memeber.new(memeber_params)
              if memeber.save
                token = AuthenticationTokenService.encode( memeber.id )
                render json: { user: memeber, token: token }
              else
                render json: { error: memeber.errors.full_messages }, status: :unprocessable_entity
              end
          end

          
          private

          def memeber_params
              params.require(:memeber).permit(:email, :password)
          end

     end
  end  
end    


9.Add routes for user creation and login:
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :memebers, only: [:create]
      post '/login', to: 'authentication#create'
    end
  end
end





EXPLANANTION OF THE CODE ABOVE
******************************************************************************************************************************



Sure! Here's a step-by-step explanation of each code snippet you provided:

AuthenticationController:

This controller is responsible for handling user authentication.
The create action is used for user login.
It finds a Memeber (typo: should be Member?) by the provided email.
If the member is found and the password is authenticated, it generates a token using AuthenticationTokenService.encode and returns
it along with the member data in the JSON response.
If the member is not found or the password authentication fails, it returns an error message in the JSON response
with the status :unauthorized.
        
        
        
        
Book2sController:

This controller is used for managing books.
The index action retrieves all books from the database, including their associated authors,
and returns them in the JSON response.
The create action creates a new book using the parameters passed in book_params. If the book is saved successfully,
it returns the created book in the JSON response with the status :created.
        Otherwise, it returns the errors in the JSON response with the status :unprocessable_entity.
The destroy action finds a book by the provided ID and deletes it. If the book is not found, 
it raises ActiveRecord::RecordNotFound, which is rescued by the not_destroyed method.
The not_destroyed method is a handler for the ActiveRecord::RecordNotDestroyed exception.
                It renders an error message in the JSON response with the status :not_found.
                        
                        
                        
MemebersController:

This controller is responsible for member (user) sign-up.
The create action creates a new member based on the parameters passed in memeber_params.
If the member is saved successfully, it generates a token using AuthenticationTokenService.encode and
returns it along with the member data in the JSON response. If there are validation errors,
it returns the errors in the JSON response with the status :unprocessable_entity.
        
        
        
        
        
ApplicationController:

This is the base controller that other controllers inherit from.
It includes ActionController::HttpAuthentication::Token to provide token-based authentication functionality.
The before_action :authenticate_user is called before every action in child controllers to enforce user authentication.
The authenticate_user method is responsible for authenticating the user using the provided token.
It attempts to extract the token from the request using token_and_options(request) and then 
decodes the token using AuthenticationTokenService.decode.
If the token is valid and corresponds to an existing member, the authentication is considered successful.
If the token is invalid or the member is not found, it raises ActiveRecord::RecordNotFound, 
                which is rescued by rendering an error message in the JSON response with the status :unauthorized.
                        
                        
                        
AuthenticationTokenService:

This service class handles the encoding and decoding of JWT tokens.
It uses the HMAC-SHA256 algorithm (HS256) and a secret key (HMAC_SECRET) to encode and decode the tokens.
The encode method takes a user_id and generates a token with an expiration time of 1 minute from the current time.
The decode method takes a token and decodes it, returning the user ID extracted from the decoded token.



Routes:

The routes file configures the available routes for the API.
It defines a namespace api/v1 and sets up routes for the MemebersController (create action) and
the AuthenticationController (create action for login).
The login route is mapped to the create action in the AuthenticationController.
These code snippets together provide a basic implementation of user authentication using JWT tokens
in a Rails API application. The user can sign up, log in, and access protected endpoints by providing
the generated token in the request headers.






































































..
