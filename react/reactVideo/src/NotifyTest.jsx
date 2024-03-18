import React from 'react';
import Notification from 'react-web-notification';

export default function NotifyTest(){
  const [ignore, setIgnore] = React.useState(true);
  const [title, setTitle] = React.useState('');

  const handlePermissionGranted = () => {
    console.log('Permission Granted');
    setIgnore(false);
  };
  const handlePermissionDenied = () => {
    console.log('Permission Denied');
    setIgnore(true);
  };
  const handleNotSupported = () => {
    console.log('Web Notification not Supported');
    setIgnore(true);
  };

  const handleNotificationOnClick = (e, tag) => {
    console.log(e, 'Notification clicked tag:' + tag);
  };

  const handleNotificationOnError = (e, tag) => {
    console.log(e, 'Notification error tag:' + tag);
  };

  const handleNotificationOnClose = (e, tag) => {
    console.log(e, 'Notification closed tag:' + tag);
  };

  const handleNotificationOnShow = (e, tag) => {
    console.log(e, 'Notification shown tag:' + tag);
  };

  const handleButtonClick = () => {
    if (ignore) {
      window.Notification.requestPermission().then(function(result) {
        console.log(result); // 'granted'
        if (result === 'granted') {
          setIgnore(false);
        }
      });
    }
    setTitle('React-Web-Notification' + Math.random());
  };

  return (
    <div>
      <button onClick={handleButtonClick}>Notify me!</button>
      <Notification
        ignore={ignore && title !== ''}
        notSupported={handleNotSupported}
        onPermissionGranted={handlePermissionGranted}
        onPermissionDenied={handlePermissionDenied}
        onShow={handleNotificationOnShow}
        onClick={handleNotificationOnClick}
        onClose={handleNotificationOnClose}
        onError={handleNotificationOnError}
        timeout={5000}
        title={title}
        options={{ body: 'Notification Body' }}
      />
    </div>
  );
};