# Using puppet to prepare a web server on a remote host.


# Install nginx web server

# From update the remote repository

exec { 'update-repo':
  command => '/usr/bin/apt-get update',
  before  => Package['nginx']
}


# Install Nginx after updating the repo
package { 'nginx':
  ensure   => installed,
  provider => apt,
  before   => Service['nginx'],
  require  => Exec['update-repo']
}

# Start nginx
service { 'nginx':
  ensure    => running,
  require   => Package['nginx'],
  subscribe => [File['/etc/nginx/sites-available/default'], File['/data/web_static/current']]
}


# setup default index page
file { '/var/www/html/index.html':
  ensure  => file,
  content => 'Holberton School',
  require => Package['nginx']
}


file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => '
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        add_header X-Served-By $Hostname;
        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        location /hbnb_static {
                alias /data/web_static/current;
        }
}
',
  notify  => Service['nginx'],
  before  => Exec['substituteHostname'],
  require => Package['nginx']
}

exec { 'substituteHostname':
  command => '/bin/sed -i "s/\$Hostname/$(hostname)/g" /etc/nginx/sites-available/default',
  require => File['/etc/nginx/sites-available/default']
}




# Creating directory for the static files
file { '/data/':
  ensure       => directory,
  group        => 'ubuntu',
  owner        => 'ubuntu',
  recurse      => true,
}

exec { '/bin/mkdir -p /data/web_static/releases/; /bin/mkdir -p /data/web_static/shared/; /bin/mkdir -p /data/web_static/releases/test/': }

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '
<html>
	<body> 
		Holberton School
 	</body>
</html>
'
}


file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  notify => Service['nginx']
}

exec { '/bin/chown -RH ubuntu:ubuntu /data/':
}
