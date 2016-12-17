require 'rubygems'
require 'bundler'

Bundler.setup

#
require File.expand_path("../serv.rb",__FILE__)
#
##
ENV['RACK_ENV'] ||= 'development'
#
##
run Application
