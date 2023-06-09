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
















































































..
