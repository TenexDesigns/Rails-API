Action Cable is a framework provided by Ruby on Rails for implementing real-time, bi-directional communication 
between the client and the server using WebSocket technology.
It allows you to build interactive and real-time features in your web applications.

Action Cable is used when you need to establish a persistent connection between the client
(typically a web browser) and the server. It enables real-time updates, notifications, chat systems,
and collaborative features in your application without the need for constant polling or refreshing the page.

Here are some key use cases and benefits of using Action Cable:

Real-time updates: Action Cable enables you to push updates from the server to the connected clients in real-time.
  This is particularly useful for applications where you want to display live data, such as real-time analytics, 
  social media feeds, or collaborative editing.

Chat systems: Action Cable provides a powerful framework for building chat systems and instant messaging features.
  It allows multiple users to interact and exchange messages in real-time, creating a seamless and interactive communication experience.
  

Notifications: You can use Action Cable to send real-time notifications to users. 
  For example, you can notify users about new messages, friend requests, system events,
  or any other relevant updates without requiring manual page refreshes.

Live updates and collaboration: Action Cable enables collaborative features by allowing multiple users to 
  work on shared resources simultaneously. Changes made by one user are instantly reflected to others, 
  fostering real-time collaboration and synchronization.

Broadcasting events: Action Cable provides an easy way to broadcast events or messages to a specific channel
  or to all connected clients. This allows you to trigger actions on the client-side based on server-side events.

Action Cable integrates seamlessly with the rest of the Ruby on Rails framework,
allowing you to leverage the features and conventions of Rails while building real-time features.
It provides a familiar programming interface and leverages Rails authentication and authorization mechanisms,
making it easy to implement real-time functionality in your existing Rails application.

Overall, Action Cable simplifies the implementation of real-time features
by abstracting away the complexities of WebSocket communication and providing a high-level framework 
for handling real-time data exchange between the client and the server.






USING ACTIOABLE
**********************************************************************************************************************

To implement ActionCable in a Rails API app, you can follow these steps:

Include ActionCable: First, make sure that your Rails API includes the ActionCable module. 
  In your config/application.rb file, add:
   # config/application.rb
   require "action_cable/engine"
Configure ActionCable: In your config/environments/development.rb file, configure the ActionCable URL:
   # config/environments/development.rb
   config.action_cable.url = "ws://localhost:3000/cable"
You can also configure the allowed origins for ActionCable in the same file:

   # config/environments/development.rb
   config.action_cable.allowed_request_origins = ['http://localhost:3000']
Replace localhost:3000 with the URL of your front-end application.

Create a channel: Generate a new channel using the Rails generator. For example, let's create a ChatMessagesChannel:
   rails generate channel ChatMessages
This command will create a chat_messages_channel.rb file in the app/channels directory. 
In this file, you can define the methods for the channel, such as subscribed, unsubscribed, and any custom actions.

   # app/channels/chat_messages_channel.rb
   class ChatMessagesChannel < ApplicationCable::Channel
     def subscribed
       stream_from "chat_messages"
     end

     def unsubscribed
       # Any cleanup needed when the channel is unsubscribed
     end

     def send_message(data)
       # Process the message and broadcast it to the subscribers
       ActionCable.server.broadcast('chat_messages', message: data['message'])
     end
   end
Set up the front-end: To use ActionCable in your front-end application, you need to include the
  actioncable JavaScript package. If youre using a JavaScript bundler like Webpack, 
  you can install the package using npm or yarn:
   npm install actioncable
Then, in your JavaScript code, import the actioncable package and create a consumer:

   import { createConsumer } from 'actioncable';

   const cable = createConsumer('ws://localhost:3000/cable');
Replace ws://localhost:3000/cable with the WebSocket URL of your Rails API.

Next, create a subscription to the ChatMessagesChannel:

   const chatMessagesChannel = cable.subscriptions.create('ChatMessagesChannel', {
     received: function(data) {
       // Handle the received message
       console.log('Received message:', data.message);
     },

     sendMessage: function(message) {
       this.perform('send_message', { message });
     }
   });
Now you can use the sendMessage method to send messages through the channel:

   chatMessagesChannel.sendMessage('Hello, ActionCable!');
    
By following these steps, you can implement ActionCable in your Rails API app and use it for 
real-time communication between the server and clients. This example demonstrates a basic chat application, 
but you can customize it according to your requirements and use cases, 
such as notifications, real-time updates, or collaborative editing. medium.com






























































..
