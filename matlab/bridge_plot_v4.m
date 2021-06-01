% Plot graphs and save monthly files of meteorological data from Bridge
% is edited by Shiho Onomura (2011-12-1)
clear;

try
    c=clock;
    n=floor(datenum(c));
    c=datevec(n);
    
    % Loading data
    %urlwrite('http://www.gvc2.gu.se/TAK-DATA/RTDM/Bro/bro.txt','test');
    %data=dlmread('test',',');
    %tendata=dlmread('Z:\Klimatst\Nya\bron_2014b_10b.dat',',',4,1); % New location 20140217
    tendata=txt2mat('Z:\Klimatst\Nya\bron_2014b_10.dat',4);
    tendata(:,2:3)=abs(tendata(:,2:3));
    
    % Copy data files from Z:\ to a local folder
    copyfile('Z:\Klimatst\Nya\bron_2014b_10.dat','C:\MeteorologicalMeasurements\GVCroof\Data\bron_2014b_10.dat');
    
    
    % Import date and time (first row)

%     filename = 'Z:\Klimatst\Nya\bron_2014b_10b.dat'; % 10 min data
%     delimiter = {','};
%     startRow = 5;
%     formatSpec = '%s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%[^\n\r]';
%      formatSpec = '%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f [^\n\r]';
%           formatSpec = '%s';
% 
%     fileID = fopen(filename,'r');
%     dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'HeaderLines' ,startRow-1, ...
%     'ReturnOnError', false);
%     fclose(fileID);
%     tendata_data = dataArray{2};
%     tendata_tid = [dataArray{1:end-1}];
%     clearvars filename delimiter startRow formatSpec fileID dataArray ans;  
%     
%     t=csvread('Z:\Klimatst\Nya\bron_2014b_10.dat');
%     fn=fopen('Z:\Klimatst\Nya\bron_2014b_10.dat');
%     test=fscanf(fn,'%f')
%     t=txt2mat('Z:\Klimatst\Nya\bron_2014b_10.dat');
%     
    % Date string to serial number. Get Year, DOY, HHMM, Code
    tendata_tid_sn = datenum(tendata(:,1),tendata(:,2),tendata(:,3),tendata(:,4),tendata(:,5),tendata(:,6));

    %tendata_year = year(tendata_tid);

    % DOY
    tendata_DOY = floor(tendata_tid_sn - datenum(year(tendata_tid_sn),1,1) + 1);

    % HHMM
    tendata_HH = num2str(tendata(:,4)); tendata_MM = num2str(tendata(:,5),'%02d');
    tendata_HM = [tendata_HH tendata_MM];tendata_HM = str2num(tendata_HM);
    clear tendata_HH tendata_MM

    % Code
    tendata_code(:,1) = 110*ones(1,size(tendata,1)); 

    % Set the same file format as before (Code, Year, DOY, HHMM, met data)
    tendata = [tendata_code tendata(:,1) tendata_DOY tendata_HM tendata(:,8:end)]; % skip first row - record number

    clear tendata_DOY tendata_HM tendata_code tendata_tid tendata_tid_sn tendata_year;
    
    
        %% Convert day of year to Julian day
    
    for k=1:size(tendata,1)
        iyear=tendata(k,2);
        doy=tendata(k,3);
        A=logical(mod(iyear,4));
        B=logical(mod(iyear,100));
        C=logical(mod(iyear,400));
        leapyear=ismember(iyear,iyear(~C | (~A & B)));
        if leapyear==1
            dayspermonth=[31 29 31 30 31 30 31 31 30 31 30 31];
            i=0;
            for j=1:12
                i=i+dayspermonth(j);
                if i>=doy
                    iday=doy-(i-dayspermonth(j));
                    imonth=j;
                    break;
                end
            end
        else
            dayspermonth=[31 28 31 30 31 30 31 31 30 31 30 31];
            i=0;
            for j=1:12
                i=i+dayspermonth(j);
                if i>=doy
                    iday=doy-(i-dayspermonth(j));
                    imonth=j;
                    break;
                end
            end
        end
        hour=floor(tendata(k,4)/100);
        min=rem(tendata(k,4)/100,1)*100;
        tendata(k,1)=datenum([iyear imonth iday hour min 0]);
    end
 

    % Saving monthly files
    % Change c if a specific month should be saved (Fredrik)
    y=datevec(datenum(c)-1); %%checking the date of yesterday
%     y(2)=5;
%     c(1)=2016;
    lmonth=y(2);
    if c(2)~=y(2)
        if y(2)==12
            year1=c(1)-1;
        else
            year1=c(1);
        end
        if exist(['C:\MeteorologicalMeasurements\Bridge\Data\MonthlyFiles2011_Now\bro_10mindata_'...
                num2str(year1) '_' num2str(lmonth) '.txt'],'file')==0
            %day of year and check for leap year
            A=logical(mod(year1,4));
            B=logical(mod(year1,100));
            C=logical(mod(year1,400));
            leapyear=ismember(year1,year1(~C | (~A & B)));
            if leapyear==1
                dayspermonth=[31 29 31 30 31 30 31 31 30 31 30 31];
            else
                dayspermonth=[31 28 31 30 31 30 31 31 30 31 30 31];
            end
            
            if y(2)==1 % changed from c to y by Fredrik 20120402
                DOYstart=1;
                DOYend=dayspermonth(1);
            else
                DOYstart=sum(dayspermonth(1:lmonth-1))+1;
                DOYend=sum(dayspermonth(1:lmonth));
            end
            
            rowstosave=find(tendata(:,2)==year1 & tendata(:,3)>=DOYstart & tendata(:,3)<=DOYend);
            tendata1=tendata(rowstosave,:);
            monthtendata=NaN(length(rowstosave),45);
            
            % Order of some data is changed following the header.
            for l=1:12 % Shiho, what is this?
                if (l==8 || l==9 || l==10)
                    monthtendata(:,l+6)=tendata1(:,l);
                elseif l==11
                    monthtendata(:,l+9)=tendata1(:,l);
                elseif l==12
                    monthtendata(:,l+5)=tendata1(:,l);
                else
                    monthtendata(:,l)=tendata1(:,l);
                end
            end
            
            %         saving only valid columns and rows (20130501), Fredrik
            monthtendata=tendata(rowstosave,:);
            
            %Save as monthly test files
            textformat='%4s %4s %3s %4s %10s %10s %13s %9s %9s %12s %8s %8s %11s %10s %9s %8s %20s %19s %18s %10s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s';
            numformat='%3d %4d %3d %4d %6.1f %6.1f %6.1f %6.3f %6.3f %6.3f %6.2f %6.2f %6.1f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.3f %6.3f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f';
            
            fn2=fopen(['C:\MeteorologicalMeasurements\Bridge\Data\MonthlyFiles2011_Now\bro_10mindata_' num2str(year1) '_' num2str(lmonth) '.txt'],'w');
            fprintf(fn2,textformat,'Jday','YYYY','DOY','HHMM','Wd_min','Wd_avg','Wd_max','Ws_min','Ws_avg','Ws_max','Ta','RH','P'...
                ,'R_amount','R_time','R_intens','H_amount','H_time','H_intens','Ws_vec_avg','Wd_vec_avg','Wd_vec_SD','temp2','temp3','temp1','Waterlevel','Wd_min_SD','Wd_avg_SD'...
                ,'Wd_max_SD','Ws_min_SD','Ws_avg_SD','Ws_max_SD','Ta_SD','RH_SD','P_SD','R_amount_SD','R_time_SD','R_intens_SD','H_amount_SD','H_time_SD','H_intens_SD','temp2_SD'...
                ,'temp3_SD','Waterlevel_SD','None');
            
            fprintf(fn2,'\r\n');
            for p=1:length(monthtendata)
                fprintf(fn2,numformat,monthtendata(p,:));
                fprintf(fn2,'\r\n');
            end
            fclose(fn2);
            f=ftp('pc70.gvc.gu.se','urban-net');
            cd(f,'public_html');
            cd(f,'Bridgedata');
            mput(f,['C:\MeteorologicalMeasurements\Bridge\Data\MonthlyFiles2011_Now\bro_10mindata_' num2str(year1) '_' num2str(lmonth) '.txt']);
            
        end
    end
    
    bridge_plot_english_v3(n,tendata)
    bridge_plot_swedish_v3(n,tendata)
    exit;
    
catch err
    msg=getReport(err);
    setpref('Internet','SMTP_Server','smtp.gu.se')
    
    setpref('Internet','E_mail','per.weslien@gu.se')
    sendmail('per.weslien@gu.se','Error in bridge_plot_v3.m',msg)
    
    setpref('Internet','E_mail','fredrikl@gvc.gu.se')
    sendmail('frans.olofson@gu.se','Error in bridge_plot_v3.m',msg)
    disp('error')
    exit;
end


%%     %     %% Plot initialisation MOVED TO SUBFUNCTIONS
%     startday=n-3;
%     X1=startday:10/1440:n+1;
%     plotdata=NaN(length(X1),size(tendata,2));
%     plotdata(:,1)=X1';
%     index=1;
%     for i=1:size(plotdata,1)
%         line2=find(plotdata(index,1)==tendata(:,1));
%         if line2>1
%             if size(tendata,1)>index
%                 plotdata(i,:)=tendata(line2,:);
%                 index=index+1;
%             end
%         end
%     end
%
%     figure1 = figure('Position',[50 50 460 900],'color',[1 1 1]);
%
%     xlabels={'0',' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
%     ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
%     ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
%     ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'};
%     xlabels2={' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
%     ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
%     ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
%     ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '};
%
%     tsize=10;
%     asize=9;
%     ysize=9;
%
%     %% Temperature
%     axes1 = axes('Parent',figure1,...
%         'YLim',[-10 40],...
%         'XLim',[n-3 n+1],...
%         'Position',[0.12 0.89 0.85 0.08],...
%         'FontSize',asize,...
%         'XTickLabel',xlabels2,...
%         'XTick',n-3:2/24:n+1,...
%         'YTickLabel',[-10 0 10 20 30 40],...
%         'YTick',-10:10:40,...
%         'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Air temperature at two heights and measured by WXT520','FontSize', tsize);
%     plot1=plot(plotdata(:,1),plotdata(:,20),plotdata(:,1),plotdata(:,22),plotdata(:,1),plotdata(:,11));
%     set(plot1(1),'DisplayName','100 masl','Color',[1 0 0],'LineStyle','-');
%     set(plot1(2),'DisplayName','5 masl','Color',[0 0 1],'LineStyle','-');
%     set(plot1(3),'DisplayName','120 masl (WXT520)','Color',[0 0.7 0],'LineStyle','-');
%
%     legend1 = legend(axes1,'show');
%     set(legend1,'Position',[0.515 0.866 0.05 0.01],'Orientation','horizontal','FontSize',asize,...
%         'FontName','Arial');
%     ylabel('T_a (^oC)','FontSize',ysize);
%
%     %% Relative humidity
%     axes1 = axes('Parent',figure1,...
%         'YLim',[0 100],...
%         'XLim',[n-3 n+1],...
%         'Position',[0.12 0.74 0.85 0.08],...
%         'FontSize',asize,...
%         'XTickLabel',xlabels2,...
%         'XTick',n-3:2/24:n+1,...
%         'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Relative humidity (WXT520)','FontSize', tsize);
%     plot2=plot(plotdata(:,1),plotdata(:,12));
%     set(plot2,'DisplayName','Wind Dir','Color',[0 1 0],'LineStyle','-');
%
%     ylabel('RH(%)','FontSize',ysize);
%
%     %% Pressure
%     axes1 = axes('Parent',figure1,...
%         'YLim',[980 1030],...
%         'XLim',[n-3 n+1],...
%         'Position',[0.12 0.625 0.85 0.08],...
%         'FontSize',asize,...
%         'XTickLabel',xlabels2,...
%         'XTick',n-3:2/24:n+1,...
%         'YTickLabel',[980 990 1000 1010 1020 1030],...
%         'YTick',990:10:1030,...
%         'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Pressure (WXT520)','FontSize', tsize);
%     plot1=plot(plotdata(:,1),plotdata(:,13));
%     ylabel('Pressure (hPa)','FontSize',ysize);
%
%         %% Hourly averaged windspeed and NOT Hourly maximum wind
%     axes2 = axes('Parent',figure1,...
%         'YLim',[0 30],...
%         'XLim',[n-3 n+1],...
%         'Position',[0.12 0.505 0.85 0.08],...
%         'FontSize',asize,...
%         'XTickLabel',xlabels2,...
%         'XTick',n-3:2/24:n+1,...
%         'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Wind speed','FontSize', tsize);
% %     plot2=plot(plotdata(:,1),plotdata(:,9),plotdata(:,1),plotdata(:,10));
%     plot2=plot(plotdata(:,1),plotdata(:,9));
%
% %     set(plot2(1),'DisplayName','Mean wind speed','Color',[0 0 0],'LineStyle','-');
% %     set(plot2(2),'DisplayName','Max wind speed','Color',[1 0 0],'LineStyle','-');
% %     legend2 = legend(axes2,'show');
% %     set(legend2,'Position',[0.50 0.490 0.10 0.01],'Orientation','horizontal','FontSize',6,...
% %         'FontName','Arial');
%     ylabel('Wspd (m s^{-1})','FontSize',ysize);
%
%     %% Winddirection
%     axes3 = axes('Parent',figure1,...
%         'YLim',[0 360],...
%         'XLim',[n-3 n+1],...
%         'Position',[0.12 0.38 0.85 0.08],...
%         'FontSize',asize,...
%         'XTickLabel',xlabels2,...
%         'YTickLabel',[0 90 180 270 360],...
%         'YTick',0:90:360,...
%         'XTick',n-3:2/24:n+1,...
%         'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Wind direction','FontSize', tsize);
%     plot3=plot(plotdata(:,1),plotdata(:,25));
%     set(plot3,'DisplayName','Wind Dir','Color',[0 0 1],'Marker','.');
%     % legend3 = legend(axes3,'show');
%     % set(legend3,'Position',[0.87 0.58 0.10 0.01],'FontSize',4,...
%     %     'FontName','Arial');
%     ylabel('WDir ( ^o )','FontSize',ysize);
%
%     %% Precipitation
%     axes3 = axes('Parent',figure1,...
%         'YLim',[0 3],...
%         'XLim',[n-3 n+1],...
%         'Position',[0.12 0.285 0.85 0.05],...
%         'FontSize',asize,...
%         'XTickLabel',xlabels2,...
%         'YTickLabel',[0 1 2 3],...
%         'YTick',0:1:3,...
%         'XTick',n-3:2/24:n+1,...
%         'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Precipitation','FontSize', tsize);
%     plot3=bar(plotdata(:,1),plotdata(:,16)/6);
%     ylabel('mm / 10min','FontSize',ysize);
%
%     %% Hail
%     axes3 = axes('Parent',figure1,...
%         'YLim',[0 50],...
%         'XLim',[n-3 n+1],...
%         'Position',[0.12 0.195 0.85 0.05],...
%         'FontSize',asize,...
%         'XTickLabel',xlabels2,...
%         'YTickLabel',[0 25 50],...
%         'YTick',0:25:50,...
%         'XTick',n-3:2/24:n+1,...
%         'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Hail','FontSize', tsize);
%     plot3=plot(plotdata(:,1),plotdata(:,19)/6);
%     ylabel('Hail (hits/cm^2)','FontSize',ysize);
%
% %% Water level
%     axes5 = axes('Parent',figure1,...
%         'YLim',[-100 100],...
%         'XLim',[n-3 n+1],...
%         'Position',[0.12 0.07 0.85 0.08],...
%         'FontSize',asize,...
%         'XTickLabel',xlabels,...
%         'XTick',n-3:2/24:n+1,...
%         'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Mean sea surface level','FontSize', tsize);
%
% %     plot5=bar(plotdata(:,1),plotdata(:,23));
%     % set(plot5,'DisplayName','Water Level',[0 0 0],'LineStyle','-');
%     text(n-3+1,0,'CURRENTLY UNAVAILABLE')
%     % Create ylabel
%     ylabel('Sea level (m)','FontSize',ysize);
%     % Create xlabel
%     xlabel('Time (h)','FontSize',ysize);
%
%     %% Dates labes
%     text(n-3+3.2,-250,datestr(n,29),'FontSize',tsize)
%     text(n-3+2.2,-250,datestr(n-1,29),'FontSize',tsize)
%     text(n-3+1.2,-250,datestr(n-2,29),'FontSize',tsize)
%     text(n-3+0.2,-250,datestr(n-3,29),'FontSize',tsize)
%     %% Save plot for web
%     savtitle=['Bridge_',datestr(round(n),30),'.png'];
%     PlotDir=fullfile('C:\MeteorologicalMeasurements\Bridge\Plot\Figures');
%     figurea=fullfile(PlotDir,savtitle);
%     set(figure1,'PaperPositionMode','auto')
%     print(figure1,'-dpng',figurea)
%
%     webtitle='Bridge_plot.png';
%     PlotDir1=fullfile('C:\MeteorologicalMeasurements\Bridge\Plot');
%     figurea1=fullfile(PlotDir1,webtitle);
%
%     set(figure1,'PaperPositionMode','auto')
%     print(figure1,'-dpng',figurea1)
%
%     f=ftp('pc70.gvc.gu.se','urban-net');
%     cd(f,'public_html');
%     mput(f,'Bridge_plot.png');
%
%     % Tablefigure
%     last=size(tendata,1);
%     fsize=5;
%     figure2 = figure('Position',[500 200 294 100],'color',[1 1 1]);
%         annotation(figure2,'textbox',[0.00 0.9 0.85 0.1],...
%     'String',['Last downloaded data at:     ' datestr(tendata(last,1),'mmmm dd, yyyy HH:MM')],...
%     'LineStyle','none','FontName','Verdana','FontSize',fsize,'FontWeight','bold');
%     annotation(figure2,'textbox',[0.00 0.75 0.85 0.1],...
%     'String',{'Air Temperature at 120 masl: '
%               'Relative Humidity at 120 masl: '
%               'Wind speed at 120 masl:      '
%               'Wind direction at 120 masl:  '
%               'Pressure at 120 masl: '
%               'Precepitation (rain):    '
%               'Waterlevel:'},...
%     'LineStyle','none','FontName','Verdana','FontSize',fsize);
%     annotation(figure2,'textbox',[0.55 0.75 0.85 0.1],...
%     'String',{num2str(tendata(last,11),'%6.1f')
%               num2str(tendata(last,12),'%6.1f')
%               num2str(tendata(last,9),'%6.1f')
%               num2str(tendata(last,25),'%6.1f')
%               num2str(tendata(last,13),'%6.1f')
%               num2str(tendata(last,14),'%6.0f')
%               'NA'},... %num2str(tendata(last,23),'%6.1f')},...
%     'LineStyle','none','FontName','Verdana','FontSize',fsize,'FontWeight','bold');
%     annotation(figure2,'textbox',[0.73 0.75 0.85 0.1],...
%     'String',{' °C'
%               ' %'
%               ' m/s'
%               ' °'
%               ' hPa'
%               ' mm/10 min'
%               ' cm'},...
%     'LineStyle','none','FontName','Verdana','FontSize',fsize);
%
%     webtitle='Bridgetable_plot.png';
%     PlotDir1=fullfile('C:\MeteorologicalMeasurements\Bridge\Plot');
%     figurea2=fullfile(PlotDir1,webtitle);
%
%     set(figure2,'PaperPositionMode','auto')
% %     saveas(figure (2), figurea2)
%     print(figure2,'-dpng',figurea2)
%
%     f=ftp('pc70.gvc.gu.se','urban-net');
%     cd(f,'public_html');
%     mput(f,'Bridgetable_plot.png');
%
