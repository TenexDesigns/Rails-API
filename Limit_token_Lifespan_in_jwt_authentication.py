To limit the life span of a JWT token in a Rails API application, you need to set the expiration time when creating the token. You can do this by adding an exp (expiration) claim to the JWT payload. Here's an example of how to implement it using the jwt gem:

Add the jwt gem to your Gemfile and run bundle install:
gem 'jwt'
Create a file called json_web_token.rb inside the app/lib directory (you may need to create the lib directory if it doesn't exist):
# app/lib/json_web_token.rb
class JsonWebToken
  SECRET_KEY = Rails.application.secrets.secret_key_base.to_s

  def self.encode(payload, exp = 24.hours.from_now)
    payload[:exp] = exp.to_i
    JWT.encode(payload, SECRET_KEY)
  end

  def self.decode(token)
    decoded = JWT.decode(token, SECRET_KEY).first
    HashWithIndifferentAccess.new(decoded)
  rescue JWT::DecodeError => e
    Rails.logger.error "JWT Error: #{e.message}"
    nil
  end
end
In this example, the encode method accepts an optional exp parameter with a default value of 24 hours from now.
The expiration time is added to the payload, and the token is generated using the JWT.encode method. 
To decode the token and check for expiration, the decode method is used.

Now, when you create a token, it will have a limited life span, and you can customize the expiration time by passing a different value for the exp parameter.

To use this token generation and verification in your authentication logic, you can follow these steps:

In your AuthenticationController, use the JsonWebToken.encode method to generate a token when the user logs in successfully:
class AuthenticationController < ApplicationController
  skip_before_action :authorized, only: [:create]

  def create
    # Your login logic here
    # If the user is authenticated, create a token
    token = JsonWebToken.encode(user_id: @user.id)
    render json: { token: token }
  end
end
In your ApplicationController, use the JsonWebToken.decode method to verify the token and check for expiration:
class ApplicationController < ActionController::API
  before_action :authorized

  def authorized
    render json: { error: 'Please log in' }, status: :unauthorized unless logged_in?
  end

  def logged_in?
    current_user.present?
  end

  def current_user
    return nil unless auth_header.present?
    token = auth_header.split(' ')[1]
    decoded_token = JsonWebToken.decode(token)
    return nil unless decoded_token
    @current_user ||= User.find_by(id: decoded_token[:user_id])
  end

  def auth_header
    request.headers['Authorization']
  end
end
With this implementation, the JWT tokens will have a limited life span, 
and any expired tokens will be rejected during the authentication process medium.com.
                                                                     
