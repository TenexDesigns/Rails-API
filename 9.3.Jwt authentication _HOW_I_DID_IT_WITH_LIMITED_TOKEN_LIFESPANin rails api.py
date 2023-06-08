


controllers/api/vi/authentication_controller.rb

module Api
    module V1
     
    
        class AuthenticationController < ApplicationController
            require ('D:\ruby\ruby1\nile\nile\lib\json_web_token.rb')
            skip_before_action :authorized, only: [:create]

            def create
                member = Memeber.find_by(email: params[:email])
                if member && member.authenticate(params[:password])
                  token = JsonWebToken.encode({ user_id: member.id })
                  render json: { token: token }
                else
                  render json: { error: 'Invalid email or password' }, status: :unauthorized
                end
            end





        end


    end

end    


  

controllers/api/vi/memebers_controller.rb

module Api
    module V1
  


       class MemebersController < ApplicationController
            skip_before_action :authorized, only: [:create]
            def create
                memeber = Memeber.new(memeber_params)
                if memeber.save
                  token = JsonWebToken.encode({ user_id: memeber.id })
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





controllers/api/vi/application_controller.rb

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
        @current_user ||= User.find_by(id: decoded_token[:memeber_id])
    end
    
    def auth_header
        request.headers['Authorization']
    end
  


end






app/lib/json_web_token.rb

class JsonWebToken
    SECRET_KEY = Rails.application.secrets.secret_key_base.to_s
  
    def self.encode(payload, exp = 1.minute.from_now)
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








































































...
