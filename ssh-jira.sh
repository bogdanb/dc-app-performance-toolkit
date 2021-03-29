#!/bin/sh
export BASTION_IP=54.217.15.225
export NODE_IP=10.0.23.14
export SSH_OPTS='-o ServerAliveInterval=60 -o ServerAliveCountMax=30'
ssh ${SSH_OPTS} -o "proxycommand ssh -W %h:%p ${SSH_OPTS} ec2-user@${BASTION_IP}" ec2-user@${NODE_IP}
