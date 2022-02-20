<?php
namespace NethServer\Module\Dashboard\Applications;

/**
 * Nextcloud dashboard application widget
 *
 * @author Markus Neuberger
 */
class Zammad extends \Nethgui\Module\AbstractModule implements \NethServer\Module\Dashboard\Interfaces\ApplicationInterface
{

    public function getName()
    {
        return "Zammad";
    }

    public function getInfo()
    {
         // $host = explode(':',$_SERVER['HTTP_HOST']);
         $host = $this->getPlatform()->getDatabase('configuration')->getProp('zammad', 'VirtualHost');

         return array(
            'url' => "https://".$host
         );
    }
}
